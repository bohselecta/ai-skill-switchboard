"""Real browser acceptance. Render-only is an explicit restricted-environment subset.

Full mode uses the served app, real browser storage, events, and downloads. Provider
UI tests use route fixtures; no third-party account or paid model is contacted.
"""
from __future__ import annotations
import hashlib, json, os, pathlib, subprocess, sys, time, traceback
from importlib.metadata import version
from playwright.sync_api import sync_playwright, expect

ROOT=pathlib.Path(__file__).resolve().parents[1]
OUT=ROOT/'artifacts'; OUT.mkdir(exist_ok=True)
RENDER=os.environ.get('SWITCHBOARD_RENDER_ONLY')=='1'
BASE=os.environ.get('SWITCHBOARD_URL','http://127.0.0.1:4173')
EDITION_FILTER=os.environ.get('SWITCHBOARD_TEST_EDITION')
results=[]; measures=[]

def record(name,fn):
    start=time.perf_counter()
    try:
        fn(); results.append({'name':name,'status':'passed','seconds':round(time.perf_counter()-start,3)})
        print('PASS',name,flush=True)
    except Exception as e:
        results.append({'name':name,'status':'failed','error':f'{type(e).__name__}: {e}','traceback':traceback.format_exc(),'seconds':round(time.perf_counter()-start,3)})
        print('FAIL',name, str(e),flush=True)
        raise

def click(page, action, id=None):
    selector=f'[data-action="{action}"]'+(f'[data-id="{id}"]' if id else '')
    page.locator(selector).filter(visible=True).first.click()

def close(page):
    if page.locator('dialog').evaluate('(d)=>d.open'):page.keyboard.press('Escape')

def open_app(page,edition):
    start=time.perf_counter()
    if RENDER:page.set_content((ROOT/'dist'/f'skill-switchboard-{edition}.html').read_text(),wait_until='load')
    else:page.goto(f'{BASE}/{edition}/',wait_until='networkidle')
    expect(page.locator('#app .workspace')).to_be_visible()
    measures.append({'edition':edition,'load_to_workspace_ms':round((time.perf_counter()-start)*1000),
                     'mode':'render-only' if RENDER else 'served-origin'})

def no_overflow(page):
    assert page.evaluate('document.documentElement.scrollWidth <= innerWidth + 1'), 'Horizontal page overflow'
    assert page.locator('img').evaluate_all('(imgs)=>imgs.every(i=>i.complete && i.naturalWidth>0)'), 'Broken image'
    if page.locator('dialog').evaluate('(d)=>d.open'):
        assert page.locator('dialog').evaluate('(d)=>d.scrollWidth<=d.clientWidth+1'), 'Horizontal dialog overflow'

def screenshot(page,name):
    page.screenshot(path=str(OUT/f'{name}.png'),full_page=True)

with sync_playwright() as pw:
    executable=os.environ.get('BROWSER_EXECUTABLE')
    browser=pw.chromium.launch(headless=True,**({'executable_path':executable} if executable else {}))
    browser_version=browser.version
    try:
        for edition in ['chatgpt','claude','gemini']:
            if EDITION_FILTER and edition!=EDITION_FILTER:continue
            context=browser.new_context(viewport={'width':1440,'height':1000},reduced_motion='reduce',accept_downloads=True)
            page=context.new_page();page.set_default_timeout(8000);errors=[]
            page.on('pageerror',lambda e:errors.append(str(e)))
            open_app(page,edition)
            def onboarding():
                expect(page.get_by_role('heading',name='A calmer way to work with AI.')).to_be_visible()
                no_overflow(page);screenshot(page,f'{edition}-onboarding')
                page.get_by_role('button',name='Explore a sample board').click()
                expect(page.locator('.skill-tile')).to_have_count(6)
                expect(page.locator('.decision-row')).to_have_count(2)
                no_overflow(page);screenshot(page,f'{edition}-board')
            record(f'{edition}: onboarding and six real skill queues',onboarding)
            def skill_chat():
                page.locator('.skill-tile').filter(has_text='Reply desk').first.click()
                expect(page.locator('.skill-chat-shell')).to_be_visible()
                expect(page.get_by_role('heading',name="I'm Reply desk.")).to_be_visible()
                expect(page.get_by_text('I still need to know:',exact=True)).to_be_visible()
                f=page.locator('form[data-form="skill-chat"]')
                f.locator('[name="message"]').fill('Draft a short reply acknowledging receipt and asking for the missing date.')
                f.get_by_role('button').click()
                expect(page.locator('.chat-task-title').filter(has_text='Draft a short reply acknowledging receipt').first).to_be_visible()
                expect(page.locator('#toast')).to_contain_text('Added to Reply desk')
                no_overflow(page);screenshot(page,f'{edition}-skill-chat');close(page)
            record(f'{edition}: skill opens as a conversational multi-task station',skill_chat)
            def approve_edit():
                page.get_by_role('button',name='A reply that needs a little judgment',exact=False).first.click()
                expect(page.get_by_text('Illustrative fixture — not a live model response',exact=False)).to_be_visible()
                no_overflow(page);screenshot(page,f'{edition}-decision')
                form=page.locator('form[data-form="approve"]');form.get_by_role('button',name='Approve draft').click()
                expect(form).to_be_visible() # Native required consent prevents submission.
                form.locator('input').check();form.get_by_role('button',name='Approve draft').click()
                expect(page.get_by_text('Approved here. Still not sent anywhere.',exact=False)).to_be_visible()
                click(page,'edit-draft');page.locator('[name="draft"]').fill('A reviewed reply with no invented time or commitments.')
                page.get_by_role('button',name='Save for review').click()
                expect(page.locator('form[data-form="approve"]')).to_be_visible()
                assert page.get_by_text('Approved here. Still not sent anywhere.',exact=False).count()==0
                close(page)
            record(f'{edition}: sample review, consent, approval and edit invalidation',approve_edit)
            def capture_route_share():
                page.keyboard.press('n')
                form=page.locator('form[data-form="capture"]')
                form.locator('[name="title"]').fill('Email reply for the new project')
                form.locator('[name="body"]').fill('Please reply to this email: can you confirm a suitable time?')
                form.get_by_role('button',name='Capture & route').click()
                expect(page.get_by_text('Local rule matched:',exact=False)).to_be_visible()
                # First handoff must stop at the sharing boundary.
                click(page,'handoff');expect(page.get_by_role('heading',name='Check before sharing.')).to_be_visible()
                form=page.locator('form[data-form="sharing"]');form.locator('input').check()
                form.get_by_role('button',name='Mark this task shareable').click()
                click(page,'handoff')
                expect(page.get_by_role('textbox',name='Prepared request')).to_contain_text('TASK DATA')
                assert 'People notes' not in page.get_by_role('textbox',name='Prepared request').input_value()
                click(page,'copy-request')
                # Wait for clipboard settlement before using the dialog's return control.
                expect(page.get_by_role('textbox',name='Text to copy').or_(page.locator('#toast').filter(has_text='Copied.')).first).to_be_visible()
                # Either real clipboard or a visible manual fallback is acceptable.
                if page.get_by_role('textbox',name='Text to copy').count():
                    assert len(page.get_by_role('textbox',name='Text to copy').input_value())>300
                page.locator('#dialog').get_by_role('button',name='Back to task',exact=True).click()
                expect(page.locator('#dialog .status-pill')).to_have_text('Waiting for a draft')
                # Invalid response does not clear source or mark anything finished.
                form=page.locator('form[data-form="result"]');form.locator('textarea').fill('{"draft":')
                form.get_by_role('button').click();expect(page.locator('#dialog .dialog-message')).to_contain_text('incomplete')
                form.locator('textarea').fill(json.dumps({'summary':'Time is not agreed.','draft':'What time would work for you?','questions':['Which timezone?']}))
                form.get_by_role('button').click();expect(page.locator('form[data-form="approve"]')).to_be_visible()
                page.locator('#dialog .source-box summary').click();click(page,'edit-source')
                page.locator('form[data-form="edit-source"] [name="body"]').fill('Please reply to the corrected email. No date has been agreed.')
                page.get_by_role('button',name='Save corrected source').click()
                assert page.locator('form[data-form="approve"]').count()==0
                click(page,'handoff');expect(page.get_by_role('heading',name='Check before sharing.')).to_be_visible();close(page)
            record(f'{edition}: capture, routing, privacy, manual handoff, response recovery',capture_route_share)
            def triage_people_skills():
                click(page,'view','inbox');page.get_by_role('button',name='This one needs a human route',exact=False).click()
                form=page.locator('form[data-form="route"]');form.locator('select').select_option('decision');form.get_by_role('button').click()
                click(page,'direction-clarify');expect(page.locator('#dialog .notice').filter(has_text='Your direction:')).to_contain_text('Draft only the minimum questions')
                click(page,'local-brief');expect(page.get_by_text('Deterministic preparation brief',exact=False)).to_be_visible();close(page)
                click(page,'view','people');click(page,'person');f=page.locator('form[data-form="person"]')
                f.locator('[name="name"]').fill('Mina Example');f.locator('[name="role"]').fill('Confirms readiness');f.locator('[name="context"]').fill('Fictional context; not shared with an AI request.')
                f.get_by_role('button').click();expect(page.locator('.person-card')).to_have_count(1)
                click(page,'view','board');click(page,'skills');page.get_by_text('Create your own skill',exact=True).click();f=page.locator('form[data-form="skill"]')
                for k,v in {'name':'Invoice brief','description':'A check before reconciliation.','keywords':'invoice','instructions':'Prepare a checkable invoice brief. Do not make payments.'}.items():f.locator(f'[name="{k}"]').fill(v)
                f.get_by_role('button').click();close(page);expect(page.locator('.skill-tile')).to_have_count(7)
            record(f'{edition}: ambiguous routing, direction, local brief, people and custom skill',triage_people_skills)
            def keyboard_mobile():
                close(page);page.keyboard.press('/');expect(page.get_by_role('searchbox',name='Search tasks')).to_be_focused()
                page.get_by_role('searchbox',name='Search tasks').fill('zz-no-match-zz');expect(page.get_by_text('Nothing in this view.')).to_be_visible()
                page.get_by_role('searchbox',name='Search tasks').fill('');click(page,'capture')
                for _ in range(20):
                    page.keyboard.press('Tab');assert page.evaluate('document.activeElement.closest("dialog") !== null'), 'Modal focus escaped'
                close(page);click(page,'view','board');page.set_viewport_size({'width':390,'height':844});no_overflow(page);screenshot(page,f'{edition}-mobile')
                page.locator('.skill-tile').first.click();no_overflow(page);screenshot(page,f'{edition}-mobile-drawer');close(page)
                assert not errors, errors
            record(f'{edition}: keyboard focus, search, reduced motion and mobile layout',keyboard_mobile)
            if not RENDER:
                def persistence_download_restore():
                    page.set_viewport_size({'width':1440,'height':1000});page.reload(wait_until='networkidle');expect(page.locator('.skill-tile')).to_have_count(7)
                    click(page,'view','inbox');page.get_by_role('button',name='A reply that needs a little judgment',exact=False).first.click()
                    f=page.locator('form[data-form="approve"]');f.locator('input').check();f.get_by_role('button').click()
                    expect(page.get_by_text('Approved here. Still not sent anywhere.',exact=False)).to_be_visible();close(page)
                    with page.expect_download() as info:click(page,'view','setup');click(page,'export')
                    backup=OUT/f'{edition}-fixture-backup.json';info.value.save_as(backup)
                    data=json.loads(backup.read_text());assert any(t['status']=='approved' for t in data['tasks'])
                    click(page,'import');page.locator('#file-input').set_input_files(str(backup));click(page,'confirm-restore')
                    expect(page.locator('#toast')).to_contain_text('Backup restored.')
                    restored=page.evaluate('(key)=>JSON.parse(localStorage.getItem(key))',f'skill-switchboard:{edition}:v1')
                    assert all(t['sensitivity']=='private' and t['status']!='approved' for t in restored['tasks'])
                    # Independent edition storage; navigation cannot silently merge boards.
                    other='gemini' if edition!='gemini' else 'chatgpt';page.goto(f'{BASE}/{other}/',wait_until='networkidle')
                    expect(page.get_by_role('heading',name='A calmer way to work with AI.')).to_be_visible()
                record(f'{edition}: actual persistence, download, safe restore and edition isolation',persistence_download_restore)
            context.close()
        if not RENDER and not EDITION_FILTER:
            context=browser.new_context(viewport={'width':1440,'height':1000});page=context.new_page();page.set_default_timeout(8000)
            def corruption_recovery():
                page.goto(BASE+'/chatgpt/',wait_until='networkidle');close(page)
                page.evaluate("localStorage.setItem('skill-switchboard:chatgpt:v1','{broken')");page.reload(wait_until='networkidle')
                expect(page.get_by_text('Your saved board could not be read.',exact=False)).to_be_visible()
                assert page.evaluate("localStorage.getItem('skill-switchboard:chatgpt:v1')")=='{broken'
                click(page,'reset');page.locator('[name="confirmation"]').fill('RESET');page.get_by_role('button',name='Clear this local board').click()
                page.get_by_role('button',name='Explore a sample board').click()
                expect(page.locator('.skill-tile')).to_have_count(6)
            record('storage: corrupt data preserved until explicit reset',corruption_recovery)
            def stale_tab():
                other=context.new_page();other.goto(BASE+'/chatgpt/',wait_until='networkidle')
                click(other,'capture');other.locator('[name="title"]').fill('Unsaved work in second tab');other.locator('[name="body"]').fill('Please reply with an honest answer.')
                click(page,'capture');page.locator('[name="title"]').fill('Saved work in first tab');page.locator('[name="body"]').fill('Please reply with a date to confirm.');page.get_by_role('button',name='Capture & route').click()
                expect(page.locator('#dialog-title')).to_have_text('Saved work in first tab')
                other.get_by_role('button',name='Capture & route').click();expect(other.locator('#dialog .dialog-message')).to_contain_text('Another tab')
                assert other.locator('[name="title"]').input_value()=='Unsaved work in second tab'
                other.close();close(page)
            record('storage: stale-tab write rejected while unsaved text survives',stale_tab)
            def malicious_and_quota():
                click(page,'capture');f=page.locator('form[data-form="capture"]');f.locator('[name="title"]').fill('<img src=x onerror=alert(1)>');f.locator('[name="body"]').fill('Please reply to <script>alert(1)</script> as plain text.');f.get_by_role('button',name='Capture & route').click()
                expect(page.locator('#dialog-title')).to_have_text('<img src=x onerror=alert(1)>')
                assert page.locator('#dialog img').count()==0;assert '<img' in page.locator('#dialog-title').inner_text();close(page)
                before=page.evaluate("localStorage.getItem('skill-switchboard:chatgpt:v1')")
                page.evaluate("() => { window.originalSet=Storage.prototype.setItem;Storage.prototype.setItem=function(){throw new DOMException('quota','QuotaExceededError')}; }")
                click(page,'capture');f=page.locator('form[data-form="capture"]');f.locator('[name="title"]').fill('Quota recovery');f.locator('[name="body"]').fill('Please reply without losing existing work.');f.get_by_role('button',name='Capture & route').click()
                expect(page.locator('#dialog .dialog-message')).to_contain_text('could not save');assert before==page.evaluate("localStorage.getItem('skill-switchboard:chatgpt:v1')")
                page.evaluate('() => { Storage.prototype.setItem=window.originalSet; }');close(page)
            record('security: escaped hostile content and failed-save recovery',malicious_and_quota)
            context.close()
            def api_ui():
                ctx=browser.new_context(viewport={'width':1440,'height':1000});p=ctx.new_page();calls=[]
                ctx.route('**/api/status',lambda r:r.fulfill(json={'csrf':'browser-fixture','providers':{'chatgpt':{'configured':True,'model':'fixture-model'}}}))
                def response(route):
                    calls.append(route.request.post_data_json)
                    if len(calls)==1:route.fulfill(status=429,json={'error':'Fixture rate limit. No automatic retry.'})
                    else:route.fulfill(json={'result':{'summary':'Fixture, not a live model.','draft':'A complete fixture draft for human review.','questions':[]},'model':'fixture-model'})
                ctx.route('**/api/generate',response);p.goto(BASE+'/chatgpt/',wait_until='networkidle');p.get_by_role('button',name='Explore a sample board').click()
                click(p,'view','inbox');p.get_by_role('button',name='Turn the discussion into next steps',exact=False).click();click(p,'generate');assert len(calls)==0
                expect(p.get_by_text('Separate provider API charges may apply.',exact=False)).to_be_visible();click(p,'confirm-generate');expect(p.locator('#dialog .status-pill')).to_have_text('Needs help');assert len(calls)==1
                click(p,'retry');click(p,'generate');click(p,'confirm-generate');expect(p.locator('form[data-form="approve"]')).to_be_visible();assert len(calls)==2
                assert calls[0]['task']['sensitivity']=='shareable';assert not p.get_by_text('Approved here.',exact=False).count();ctx.close()
            record('API UI fixtures: billing gate, error, deliberate retry and mandatory review',api_ui)
    except Exception:
        traceback.print_exc()
        try:screenshot(page,'failure')
        except Exception:pass
    finally:
        browser.close()
        digest=hashlib.sha256()
        for file in sorted([*ROOT.glob('shared/*'),ROOT/'server.mjs',ROOT/'tests/browser.py']):
            if file.is_file():digest.update(str(file.relative_to(ROOT)).encode());digest.update(file.read_bytes())
        try:revision=subprocess.check_output(['git','rev-parse','HEAD'],cwd=ROOT,text=True,stderr=subprocess.DEVNULL).strip()
        except Exception:revision='uncommitted-local-source'
        report={'mode':'render-only; no served-origin persistence or provider calls' if RENDER else 'served Chromium; provider responses mocked',
                'revision':revision,'source_sha256':digest.hexdigest(),'browser':browser_version,'playwright':version('playwright'),
                'viewport_desktop':'1440x1000','viewport_mobile':'390x844','reduced_motion':True,
                'results':results,'load_observations':measures,'live_provider_calls':0,
                'limitations':['No authenticated provider-account install test','No live model quality or latency test','No participant study','Not an independent accessibility certification']}
        (OUT/'browser-report.json').write_text(json.dumps(report,indent=2)+'\n')
        print(json.dumps({'passed':sum(r['status']=='passed' for r in results),'failed':sum(r['status']=='failed' for r in results),'mode':report['mode']}),flush=True)
        if not results or any(r['status']=='failed' for r in results):sys.exit(1)
