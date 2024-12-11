import subprocess
import sys
import os
import time

def run_helm_command(command, namespace=None):
    """
    执行Helm命令的函数
    
    Args:
        command (str): Helm命令
        namespace (str, optional): Kubernetes命名空间，默认为None
    """
    try:
        base_command = ['helm']
        if namespace:
            base_command.extend(['-n', namespace])
        
        base_command.extend(command.split())
        
        result = subprocess.run(
            base_command,
            check=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            universal_newlines=True
        )
        
        print("命令执行成功:")
        print(result.stdout)
        return result.stdout
        
    except subprocess.CalledProcessError as e:
        print(f"命令执行失败，错误信息：")
        print(e.stderr)
        sys.exit(1)


def wait_for_pod_ready(pod_name, namespace="default", timeout=300):
    """
    等待Pod就绪
    
    Args:
        pod_name (str): Pod名称
        namespace (str): 命名空间，默认为"default"
        timeout (int): 超时时间（秒），默认为300秒
    """
    print(f"等待Pod {pod_name} 在命名空间 {namespace} 中就绪...")
    start_time = time.time()
    
    while True:
        try:
            # 检查Pod状态
            phase_cmd = ["kubectl", "get", "pod", pod_name, "-n", namespace, "-o", "jsonpath={.status.phase}"]
            print(f"执行命令: {' '.join(phase_cmd)}")
            phase_result = subprocess.run(phase_cmd, check=True, capture_output=True, text=True)
            phase = phase_result.stdout.strip()
            print(f"命令输出: {phase}")
            
            # 如果Pod状态是Running，检查容器状态
            if phase == "Running":
                # 检查容器是否处于Created状态
                container_state_cmd = ["kubectl", "get", "pod", pod_name, "-n", namespace, 
                                     "-o", "jsonpath={.status.containerStatuses[*].state}"]
                print(f"执行命令: {' '.join(container_state_cmd)}")
                state_result = subprocess.run(container_state_cmd, check=True, capture_output=True, text=True)
                print(f"容器状态: {state_result.stdout}")
                
                if "running" in state_result.stdout:
                    # 检查容器是否ready
                    container_ready_cmd = ["kubectl", "get", "pod", pod_name, "-n", namespace, 
                                         "-o", "jsonpath={.status.containerStatuses[*].ready}"]
                    print(f"执行命令: {' '.join(container_ready_cmd)}")
                    ready_result = subprocess.run(container_ready_cmd, check=True, capture_output=True, text=True)
                    container_statuses = ready_result.stdout.strip().split()
                    print(f"命令输出: {ready_result.stdout}")
                    
                    if all(status == "true" for status in container_statuses):
                        print(f"Pod {pod_name} 及其所有容器已就绪!")
                        return True
                    else:
                        print("Pod运行中但容器尚未就绪，继续等待...")
                else:
                    print("容器尚未处于Running状态，继续等待...")
            else:
                print(f"Pod状态: {phase}，继续等待...")
            
            if time.time() - start_time > timeout:
                print(f"等待Pod超时（{timeout}秒）")
                return False
                
            time.sleep(5)
            
        except subprocess.CalledProcessError as e:
            error_msg = e.stderr.decode() if isinstance(e.stderr, bytes) else str(e.stderr)
            if "is waiting to start: ContainerCreating" in error_msg:
                print("容器正在创建中，继续等待...")
                time.sleep(5)
                continue
            else:
                print(f"获取Pod状态失败: {error_msg}")
                time.sleep(5)
           

def exec_into_pod(pod_name, namespace="default"):
    """
    检查Pod中的CCSEmDispatcherExe进程
    
    Args:
        pod_name (str): Pod名称
        namespace (str): 命名空间
    """
    try:
        start_time = time.time()
        first_count = 0
        retry_count = 0
        max_retries = 10
        
        while True:
            # 检查CCSEmDispatcherExe进程
            check_cmd = ["kubectl", "exec", "-n", namespace, pod_name, "--", "ps", "-ef"]
            print(f"执行命令: {' '.join(check_cmd)}")
            
            result = subprocess.run(check_cmd, capture_output=True, text=True)
            # 直接统计包含CCSEmDispatcherExe的行数
            process_count = sum(1 for line in result.stdout.splitlines() if 'CCSEmDispatcherExe' in line and 'grep' not in line)
            
            if process_count > 0:
                if first_count == 0:
                    # 第一次找到进程，记录数量
                    first_count = process_count
                    print(f"\n第一次找到 {first_count} 个CCSEmDispatcherExe进程")
                    
                    print("\n等待1秒后再次确认...")
                    time.sleep(1)
                    continue
                else:
                    # 第二次确认
                    current_count = process_count
                    print(f"\n第二次确认找到 {current_count} 个CCSEmDispatcherExe进程")
                    
                    if current_count == first_count:
                        print(f"\n两次检查结果一致 (进程数: {current_count})")
                        return current_count
                    else:
                        print(f"\n警告：两次检查结果不一致 (第一次: {first_count}, 第二次: {current_count})")
                        retry_count += 1
                        if retry_count >= max_retries:
                            print(f"\n已达到最大重试次数({max_retries})，返回最后一次检查结果")
                            return current_count
                        print(f"\n第 {retry_count} 次重试...")
                        first_count = 0  # 重置计数，重新开始检查
            
            # 检查是否超时
            if time.time() - start_time > 10:  # 10秒超时
                print("\n超过10秒仍未找到稳定的进程数量")
                return 0
            
            print(f"\n未找到进程或进程数不稳定，初次找到的进程数: {first_count}，等待1秒后重试...")
            time.sleep(1)
            
    except subprocess.CalledProcessError as e:
        print(f"命令执行失败: {e.stderr}")
        return 0
    except Exception as e:
        print(f"发生错误: {str(e)}")
        return 0
          

def count_specific_log(pod_name, namespace="default", search_text="running EM dispatcher for core", timeout=60):
    """
    查看并统计Pod中包含特定文本的日志行数，找到后再次确认
    
    Args:
        pod_name (str): Pod名称
        namespace (str): 命名空间
        search_text (str): 要搜索的文本
        timeout (int): 超时时间（秒）
    """
    try:
        start_time = time.time()
        first_count = 0
        retry_count = 0
        max_retries = 10
        
        while True:
            # 使用kubectl logs命令获取日志
            cmd = [
                "kubectl", 
                "logs", 
                "-n", 
                namespace, 
                pod_name
            ]
            
            print(f"执行命令: {' '.join(cmd)}")
            result = subprocess.run(
                cmd,
                check=True,
                capture_output=True,
                text=True
            )
            
            # 在Python中过滤包含指定文本的行
            log_lines = [line for line in result.stdout.splitlines() if search_text in line]
            count = len(log_lines)
            
            if count > 0:
                if first_count == 0:
                    # 第一次找到匹配，记录数量
                    first_count = count
                    print(f"\n第一次找到包含文本 '{search_text}' 的日志行数: {count}")
                 
                    print("\n等待1秒后再次确认...")
                    time.sleep(1)
                    continue
                else:
                    # 第二次确认
                    print(f"\n第二次确认找到包含文本 '{search_text}' 的日志行数: {count}")
                    print("\n匹配的日志内容:")
                    for line in log_lines:
                        print(line)
                    
                    if count == first_count:
                        print(f"\n两次检查结果一致 (数量: {count})")
                        return count
                    else:
                        print(f"\n警告：两次检查结果不一致 (第一次: {first_count}, 第二次: {count})")
                        retry_count += 1
                        if retry_count >= max_retries:
                            print(f"\n已达到最大重试次数({max_retries})，返回最后一次检查结果")
                            return count
                        print(f"\n第 {retry_count} 次重试...")
                        first_count = 0  # 重置计数，重新开始检查
            
            # 检查是否超时
            if time.time() - start_time > timeout:
                print(f"\n超过{timeout}秒仍未找到匹配的日志")
                return 0
                
            print(f"\n未找到匹配的日志，等待1秒后重试...")
            time.sleep(1)
            
    except subprocess.CalledProcessError as e:
        print(f"获取日志失败: {e.stderr}")
        return 0

def check_and_delete_helm_release(release_name="ccsrt-l2rt-cran1", namespace="cran1"):
    """
    检查并删除指定的Helm Release
    
    Args:
        release_name (str): Helm Release名称
        namespace (str): 命名空间
    """
    try:
        # 检查helm release是否存在
        check_cmd = f"list -n {namespace}"  # 修改这里，移除了release_name参数
        print(f"\n检查Helm Release {release_name}...")
        result = run_helm_command(check_cmd)
        
        if release_name in result:
            print(f"找到Helm Release {release_name}，准备删除...")
            # 删除helm release
            delete_cmd = f"delete -n {namespace} {release_name}"
            run_helm_command(delete_cmd)
            
            # 等待Pod终止
            pod_name = "ccsrt-up-0"
            print(f"\n等待Pod {pod_name} 终止...")
            while True:
                try:
                    cmd = ["kubectl", "get", "pod", pod_name, "-n", namespace]
                    print(f"执行命令: {' '.join(cmd)}")
                    result = subprocess.run(cmd, capture_output=True, text=True)
                    
                    if result.returncode != 0:  # Pod不存在时返回非0
                        print(f"Pod {pod_name} 已终止")
                        break
                        
                    print("Pod仍在运行，继续等待...")
                    time.sleep(5)
                    
                except subprocess.CalledProcessError:
                    print(f"Pod {pod_name} 已终止")
                    break
        else:
            print(f"未找到Helm Release {release_name}")
            
    except Exception as e:
        print(f"检查或删除Helm Release时出错: {str(e)}")
        sys.exit(1)


            
def main():
    # Pod名称和命名空间
    pod_name = "ccsrt-up-0"
    expected_count = 20  # 期望的日志条数
    namespace = "cran1"

    while True:  # 添加无限循环
        try:
            # 在开始部署前先检查并清理旧的部署
            check_and_delete_helm_release()
            
            # 执行Helm命令
            run_helm_command("upgrade --namespace=cran1 "
                        "--set image.ccsrtl2rt.registry=rcp-docker-testing-virtual.artifactory-espoo2.int.net.nokia.com "
                        "--set image.ccsrtl2rt.repository=ccs-rt/ccs-rt-dpm-test "
                        "--set image.ccsrtl2rt.tag=3.7.0-276-g8b24b59a0 "
                        "--set image.ccsrtltel2.registry=rcp-docker-testing-virtual.artifactory-espoo2.int.net.nokia.com "
                        "--set image.ccsrtltel2.repository=ccs-rt/ccs-rt-dpm-trs-test "
                        "--set image.ccsrtltel2.tag=3.7.0-276-g8b24b59a0 "
                        "--set image.ccsrtfddmacps.registry=rcp-docker-testing-virtual.artifactory-espoo2.int.net.nokia.com "
                        "--set image.ccsrtfddmacps.repository=ccs-rt/ccs-rt-dpm-test "
                        "--set image.ccsrtfddmacps.tag=3.7.0-276-g8b24b59a0 "
                        "--set image.ccsrtl2hi.registry=rcp-docker-testing-virtual.artifactory-espoo2.int.net.nokia.com "
                        "--set image.ccsrtl2hi.repository=ccs-rt/ccs-rt-dpm-trs-test "
                        "--set image.ccsrtl2hi.tag=3.7.0-276-g8b24b59a0 "
                        "--set-string nwmgmtContainerInclude=false "
                        "--set-string l2hiContainerInclude=false "
                        "--set-string l2rtContainerInclude=true "
                        "--set-string l1ContainerInclude=false "
                        "--set-string IsCaseEnableEMTrace=no "
                        "--set-string ccsrtl2hi.resources.limits.sharedNum_cpuPooler=800 "
                        "--set-string ccsrtl2rt.resources.limits.sharedNum_cpuPooler=500 "
                        "--set mirroringIndInterval=2 "
                        "--set mirroringRate=1 "
                        "--set global.name_convention.statefulset_prefix=ccsrt "
                        "-f values-override.yaml "
                        "-f ../rcp-pod-override-network.yaml "
                        "--install ccsrt-l2rt-cran1 .")    
            
            # 等待Pod就绪
            if wait_for_pod_ready(pod_name, namespace):
                try:
                    # Pod就绪后检查进程
                    print(f"正在检查Pod {pod_name}中的进程...")
                    exec_into_pod(pod_name, namespace)
                except Exception as e:
                    print(f"进程检查异常终止: {str(e)}")
                    continue  # 如果出错，继续下一次循环
            else:
                print("Pod未能成功启动")
                continue  # Pod未就绪，继续下一次循环
            
            # 检查日志条数
            try:
                count = count_specific_log(pod_name, namespace)
                if count < expected_count:
                    print(f"\n警告：找到的日志条数（{count}）小于期望值（{expected_count}）")
                    sys.exit(1)  # 日志条数不足就退出程序
                else:
                    print(f"\n日志条数符合预期：{count} >= {expected_count}")
                    run_helm_command("delete ccsrt-l2rt-cran1")
                    continue  # 成功后继续下一次循环
                    
            except Exception as e:
                print(f"\n检查日志条数时发生错误: {str(e)}")
                continue  # 如果出错，继续下一次循环
                
        except KeyboardInterrupt:
            print("\n检测到用户中断，正在退出...")
            sys.exit(0)
        except Exception as e:
            print(f"\n发生未预期的错误: {str(e)}")
            continue  # 如果出错，继续下一次循环


if __name__ == "__main__":
    main()
