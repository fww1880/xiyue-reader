import requests, subprocess, os
base_dir = r'C:\Users\86139\aipywork\CapEwGvvipaKTj79zEPUj'
print("🔍 获取最新失败的具体步骤...")
# 获取仓库信息
remote = subprocess.run(['git', 'remote', 'get-url', 'origin'], cwd=base_dir, capture_output=True, text=True)
remote_url = remote.stdout.strip()
if 'github.com/' in remote_url:
    parts = remote_url.split('github.com/')[1].replace('.git', '').strip()
    # 获取最近一次失败的 run
    api_url = f"https://api.github.com/repos/{parts}/actions/runs?status=failure&per_page=1"
    try:
        resp = requests.get(api_url, timeout=10)
        if resp.status_code == 200:
            runs = resp.json().get('workflow_runs', [])
            if runs:
                run = runs[0]
                run_id = run['id']
                print(f"✅ 失败运行 ID: {run_id}")
                # 获取 jobs
                jobs_url = f"https://api.github.com/repos/{parts}/actions/runs/{run_id}/jobs"
                jobs_resp = requests.get(jobs_url, timeout=10)
                if jobs_resp.status_code == 200:
                    jobs = jobs_resp.json().get('jobs', [])
                    for job in jobs:
                        print(f"\n📋 Job: {job['name']} - {job['conclusion']}")
                        print(f"   Started: {job['started_at']}")
                        print(f"   Updated: {job['completed_at']}")
                        # 获取步骤详情
                        steps = job.get('steps', [])
                        print(f"   共 {len(steps)} 个步骤:")
                        for i, step in enumerate(steps):
                            status_icon = "✅" if step['conclusion'] == 'success' else "❌" if step['conclusion'] == 'failure' else "⏳"
                            print(f"   {i+1}. {status_icon} {step['name']} - {step['conclusion']} ({step['number']}号)")
                            if step['conclusion'] == 'failure':
                                print(f"      👈 这个步骤失败了！")
                else:
                    print(f"⚠️ 获取 jobs 失败: {jobs_resp.status_code}")
            else:
                print("❌ 没有找到失败的运行记录")
        else:
            print(f"⚠️ API 请求失败: {resp.status_code}")
    except Exception as e:
        print(f"❌ 请求异常: {e}")
print("\n💡 请老板告诉我失败的是哪个步骤，我马上修复！")