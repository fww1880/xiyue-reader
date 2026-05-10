import subprocess, os, json, requests
base_dir = r'C:\Users\86139\aipywork\CapEwGvvipaKTj79zEPUj'
print("📋 尝试通过 GitHub API 获取日志...")
# 获取仓库信息
import subprocess
remote = subprocess.run(['git', 'remote', 'get-url', 'origin'], cwd=base_dir, capture_output=True, text=True)
remote_url = remote.stdout.strip()
print(f"远程仓库: {remote_url}")
# 提取 owner/repo
if 'github.com/' in remote_url:
    parts = remote_url.split('github.com/')[1].replace('.git', '').strip()
    print(f"仓库: {parts}")
    # 尝试通过 GitHub API 获取最近一次失败的 run
    api_url = f"https://api.github.com/repos/{parts}/actions/runs?status=failure&per_page=1"
    print(f"请求: {api_url}")
    try:
        resp = requests.get(api_url, timeout=10)
        if resp.status_code == 200:
            runs = resp.json().get('workflow_runs', [])
            if runs:
                run = runs[0]
                run_id = run['id']
                print(f"✅ 找到最近的失败运行: ID={run_id}")
                # 获取该运行的 jobs
                jobs_url = f"https://api.github.com/repos/{parts}/actions/runs/{run_id}/jobs"
                jobs_resp = requests.get(jobs_url, timeout=10)
                if jobs_resp.status_code == 200:
                    jobs = jobs_resp.json().get('jobs', [])
                    for job in jobs:
                        print(f"\n📋 Job: {job['name']} - {job['conclusion']}")
                        # 获取步骤详情
                        for step in job.get('steps', []):
                            if step['conclusion'] == 'failure':
                                print(f"  ❌ 失败步骤: {step['name']}")
                                # 获取该步骤的日志
                                logs_url = f"https://api.github.com/repos/{parts}/actions/jobs/{job['id']}/logs"
                                logs_resp = requests.get(logs_url, timeout=10)
                                if logs_resp.status_code == 200:
                                    log_text = logs_resp.text
                                    # 只取最后 2000 字符
                                    print(f"\n  📝 日志（最后2000字符）：")
                                    print(log_text[-2000:])
                                else:
                                    print(f"  无法获取日志: {logs_resp.status_code}")
                else:
                    print(f"⚠️ 获取 jobs 失败: {jobs_resp.status_code}")
            else:
                print("❌ 没有找到失败的运行记录")
        else:
            print(f"⚠️ API 请求失败: {resp.status_code}")
            print(f"响应: {resp.text[:500]}")
    except Exception as e:
        print(f"❌ 请求异常: {e}")
        print("\n💡 建议：请老板手动查看日志并告诉我具体错误信息")
        print("1. 打开 https://github.com/fww1880/xiyue-reader/actions")
        print("2. 点击最新的失败任务")
        print("3. 展开失败的步骤，复制错误信息发给我")