import requests
import time
import json
import math

def get_unused_coupons(token):
    """
    获取未使用的优惠券ID
    
    参数:
    token: 授权令牌
    
    返回:
    未使用的优惠券ID列表
    """
    url = "https://api.prod.testnet.anoma.net/api/v1/garapon"
    
    headers = {
        "accept": "*/*",
        "accept-encoding": "gzip, deflate, br, zstd",
        "accept-language": "zh-CN,zh;q=0.9,en;q=0.8",
        "authorization": f"Bearer {token}",
        "origin": "https://testnet.anoma.net",
        "referer": "https://testnet.anoma.net/",
        "sec-ch-ua": '"Not;A=Brand";v="99", "Google Chrome";v="139", "Chromium";v="139"',
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": '"macOS"',
        "sec-fetch-dest": "empty",
        "sec-fetch-mode": "cors",
        "sec-fetch-site": "same-site",
        "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/139.0.0.0 Safari/537.36"
    }
    
    try:
        response = requests.get(url, headers=headers)
        
        if response.status_code < 400:
            data = response.json()
            unused_coupons = [coupon["id"] for coupon in data.get("coupons", []) if coupon.get("used") == False]
            return unused_coupons
        else:
            print(f"获取优惠券失败，状态码: {response.status_code}")
            return []
    except Exception as e:
        print(f"获取优惠券时发生错误: {str(e)}")
        return []

def use_coupons(token, coupon_ids, delay=3):
    """
    使用优惠券
    
    参数:
    token: 授权令牌
    coupon_ids: 优惠券ID列表
    delay: 每次调用间隔时间(秒)
    """
    url = "https://api.prod.testnet.anoma.net/api/v1/garapon/use"
    
    headers = {
        "accept": "*/*",
        "accept-encoding": "gzip, deflate, br, zstd",
        "accept-language": "zh-CN,zh;q=0.9,en;q=0.8",
        "authorization": f"Bearer {token}",
        "content-type": "application/json",
        "origin": "https://testnet.anoma.net",
        "priority": "u=1, i",
        "referer": "https://testnet.anoma.net/",
        "sec-ch-ua": '"Not;A=Brand";v="99", "Google Chrome";v="139", "Chromium";v="139"',
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": '"macOS"',
        "sec-fetch-dest": "empty",
        "sec-fetch-mode": "cors",
        "sec-fetch-site": "same-site",
        "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/139.0.0.0 Safari/537.36"
    }
    
    total = len(coupon_ids)
    success_count = 0
    failure_count = 0
    
    print(f"开始使用优惠券，共 {total} 张未使用的优惠券")
    
    for i, coupon_id in enumerate(coupon_ids):
        try:
            payload = {"id": coupon_id}
            
            print(f"第 {i+1}/{total} 次调用")
            
            # 发送请求
            response = requests.put(url, headers=headers, json=payload)
            
            # 处理响应
            try:
                data = response.json()
                if response.status_code < 400:
                    # 成功
                    prize_amount = data.get("prize_amount", "未知")
                    print(f"优惠券 {coupon_id} 使用成功，获取 {prize_amount} 积分")
                    success_count += 1
                else:
                    # 失败
                    print(f"优惠券 {coupon_id} 使用失败")
                    failure_count += 1
            except:
                # 解析JSON失败
                print(f"优惠券 {coupon_id} 使用失败")
                failure_count += 1
            
            # 等待指定时间后再次调用
            if i < total - 1:
                print(f"等待 {delay} 秒后继续下一次调用...\n")
                time.sleep(delay)
                
        except Exception as e:
            print(f"优惠券 {coupon_id} 使用失败，错误: {str(e)}")
            failure_count += 1
            
            # 出错后等待一段时间再继续
            if i < total - 1:
                print(f"等待 {delay} 秒后重试...\n")
                time.sleep(delay)
    
    print(f"\n调用完成，总计: {total} 次，成功: {success_count} 次，失败: {failure_count} 次")

def claim_fitcoin(token, times=1, delay=1):
    """
    调用fitcoin接口
    
    参数:
    token: 授权令牌
    times: 调用次数，默认为1
    delay: 每次调用间隔时间(秒)，默认为1
    
    返回:
    获取到的fitcoin数量
    """
    url = "https://api.prod.testnet.anoma.net/api/v1/fitcoin"
    
    headers = {
        "accept": "*/*",
        "accept-encoding": "gzip, deflate, br, zstd",
        "accept-language": "zh-CN,zh;q=0.9,en;q=0.8",
        "authorization": f"Bearer {token}",
        "content-type": "application/json",
        "origin": "https://testnet.anoma.net",
        "referer": "https://testnet.anoma.net/",
        "sec-ch-ua": '"Not;A=Brand";v="99", "Google Chrome";v="139", "Chromium";v="139"',
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": '"macOS"',
        "sec-fetch-dest": "empty",
        "sec-fetch-mode": "cors",
        "sec-fetch-site": "same-site",
        "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/139.0.0.0 Safari/537.36"
    }
    
    payload = {}
    total_fitcoins = 0
    success_count = 0
    failure_count = 0
    
    # 如果只调用一次，直接调用
    if times == 1:
        try:
            print("正在调用fitcoin接口...")
            response = requests.post(url, headers=headers, json=payload)
            
            # 处理响应
            try:
                data = response.json()
                if response.status_code < 400:
                    print("fitcoin领取成功")
                    if "fitcoins" in data:
                        total_fitcoins = data["fitcoins"]
                        print(f"当前拥有 {total_fitcoins} fitcoin")
                        return total_fitcoins
                    return 0
                else:
                    print("fitcoin领取失败")
                    if "error" in data:
                        print(f"错误信息: {data['error']}")
                    return 0
            except:
                print(f"fitcoin领取失败，状态码: {response.status_code}")
                return 0
        except Exception as e:
            print(f"fitcoin领取出错: {str(e)}")
            return 0
    
    # 如果调用多次，循环调用
    print(f"开始批量领取fitcoin，计划调用 {times} 次")
    
    for i in range(times):
        try:
            print(f"第 {i+1}/{times} 次调用")
            
            # 发送请求
            response = requests.post(url, headers=headers, json=payload)
            
            # 处理响应
            try:
                data = response.json()
                if response.status_code < 400:
                    success_count += 1
                    if "fitcoins" in data:
                        total_fitcoins = data["fitcoins"]
                        print(f"领取成功，当前拥有 {total_fitcoins} fitcoin")
                else:
                    failure_count += 1
                    if "error" in data:
                        print(f"领取失败，错误: {data['error']}")
            except:
                print(f"领取失败，状态码: {response.status_code}")
                failure_count += 1
            
            # 等待指定时间后再次调用
            if i < times - 1:
                print(f"等待 {delay} 秒后继续下一次调用...\n")
                time.sleep(delay)
                
        except Exception as e:
            print(f"领取出错: {str(e)}")
            failure_count += 1
            
            # 出错后等待一段时间再继续
            if i < times - 1:
                print(f"等待 {delay} 秒后重试...\n")
                time.sleep(delay)
    
    print(f"\n领取完成，总计: {times} 次，成功: {success_count} 次，失败: {failure_count} 次")
    print(f"当前拥有 {total_fitcoins} fitcoin")
    
    return total_fitcoins

def buy_garapon(token, amount=1):
    """
    购买抽奖券
    
    参数:
    token: 授权令牌
    amount: 购买数量，默认为1
    
    返回:
    是否成功
    """
    url = "https://api.prod.testnet.anoma.net/api/v1/garapon/buy"
    
    headers = {
        "accept": "*/*",
        "accept-encoding": "gzip, deflate, br, zstd",
        "accept-language": "zh-CN,zh;q=0.9,en;q=0.8",
        "authorization": f"Bearer {token}",
        "content-type": "application/json",
        "origin": "https://testnet.anoma.net",
        "referer": "https://testnet.anoma.net/",
        "sec-ch-ua": '"Not;A=Brand";v="99", "Google Chrome";v="139", "Chromium";v="139"',
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": '"macOS"',
        "sec-fetch-dest": "empty",
        "sec-fetch-mode": "cors",
        "sec-fetch-site": "same-site",
        "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/139.0.0.0 Safari/537.36"
    }
    
    payload = {"amount": amount}
    
    try:
        print(f"正在购买 {amount} 张抽奖券...")
        response = requests.post(url, headers=headers, json=payload)
        
        # 处理响应
        try:
            data = response.json()
            if response.status_code < 400:
                print(f"成功购买 {amount} 张抽奖券")
                return True
            else:
                print(f"购买抽奖券失败")
                if "error" in data:
                    print(f"错误信息: {data['error']}")
                return False
        except:
            print(f"购买抽奖券失败，状态码: {response.status_code}")
            return False
    except Exception as e:
        print(f"购买抽奖券出错: {str(e)}")
        return False

def auto_process(token, claim_times=10, delay=1):
    """
    自动执行完整流程：领取fitcoin -> 购买抽奖券 -> 使用抽奖券
    
    参数:
    token: 授权令牌
    claim_times: 领取fitcoin的次数
    delay: 每次调用间隔时间(秒)
    """
    # 1. 领取fitcoin
    print("===== 第一步：领取fitcoin =====")
    fitcoins = claim_fitcoin(token, claim_times, delay)
    
    if fitcoins <= 0:
        print("未能获取fitcoin，流程终止")
        return
    
    # 2. 计算可以购买的抽奖券数量
    buy_amount = math.floor(fitcoins / 50)
    if buy_amount <= 0:
        print(f"当前拥有 {fitcoins} fitcoin，不足以购买抽奖券（需要50 fitcoin/张）")
        return
    
    # 3. 购买抽奖券
    print(f"\n===== 第二步：购买抽奖券 =====")
    print(f"当前拥有 {fitcoins} fitcoin，可购买 {buy_amount} 张抽奖券")
    
    success = buy_garapon(token, buy_amount)
    if not success:
        print("购买抽奖券失败，流程终止")
        return
    
    # 等待一段时间，确保抽奖券已到账
    print("等待3秒，确保抽奖券已到账...")
    time.sleep(3)
    
    # 4. 获取未使用的抽奖券
    print(f"\n===== 第三步：使用抽奖券 =====")
    unused_coupon_ids = get_unused_coupons(token)
    
    if not unused_coupon_ids:
        print("没有找到未使用的抽奖券，流程终止")
        return
    
    print(f"找到 {len(unused_coupon_ids)} 张未使用的抽奖券")
    
    # 5. 使用抽奖券
    use_coupons(token, unused_coupon_ids, delay=3)

if __name__ == "__main__":
    # 从用户提供的Headers中提取token
    token = "SFMyNTY.g2gDdAAAAAVtAAAAA2V4cGJoqUHGbQAAAANpYXRiaKfwRm0AAAADaXNzbQAAAA1hbm9tYV9iYWNrZW5kbQAAAAR0eXBlbQAAAAhtZXRhbWFza20AAAAHdXNlcl9pZmYzOGNibgYAs5EC0JgBYgABUYA.SJKYn7gx4LdZ1iL-O806WXmi40sjU1g2qsvuKE9bZrk"
    
    print("Anoma工具箱")
    print("1. 使用现有抽奖券")
    print("2. 领取fitcoin")
    print("3. 购买抽奖券")
    print("4. 自动执行完整流程（领取fitcoin -> 购买抽奖券 -> 使用抽奖券）")
    print("0. 退出")
    
    choice = input("请选择操作: ")
    
    if choice == "1":
        # 使用现有抽奖券
        print("正在获取未使用的抽奖券...")
        unused_coupon_ids = get_unused_coupons(token)
        
        if unused_coupon_ids:
            print(f"找到 {len(unused_coupon_ids)} 张未使用的抽奖券")
            
            # 使用默认3秒延迟
            delay = 3.0
            
            # 是否继续
            if input(f"是否使用这些抽奖券？延迟时间为 {delay} 秒 (y/n): ").lower() == 'y':
                # 使用抽奖券
                use_coupons(token, unused_coupon_ids, delay)
            else:
                print("操作已取消")
        else:
            print("没有找到未使用的抽奖券")
    
    elif choice == "2":
        # 领取fitcoin
        try:
            times = int(input("请输入领取次数 (1-2000): "))
            if times < 1 or times > 2000:
                print("次数超出范围，设置为默认值10")
                times = 10
                
            delay = float(input("请输入每次领取间隔时间(秒): "))
            if delay < 0.1:
                print("间隔时间太短，设置为默认值1秒")
                delay = 1.0
                
            claim_fitcoin(token, times, delay)
        except ValueError:
            print("输入无效，请输入有效的数字")
    
    elif choice == "3":
        # 购买抽奖券
        try:
            amount = int(input("请输入购买数量: "))
            if amount < 1:
                print("数量无效，至少购买1张")
            else:
                buy_garapon(token, amount)
        except ValueError:
            print("输入无效，请输入有效的数字")
    
    elif choice == "4":
        # 自动执行完整流程
        try:
            times = int(input("请输入领取fitcoin的次数 (1-2000): "))
            if times < 1 or times > 2000:
                print("次数超出范围，设置为默认值10")
                times = 10
                
            delay = float(input("请输入每次领取间隔时间(秒): "))
            if delay < 0.1:
                print("间隔时间太短，设置为默认值1秒")
                delay = 0.5
                
            auto_process(token, times, delay)
        except ValueError:
            print("输入无效，请输入有效的数字")
    
    elif choice == "0":
        print("程序已退出")
    
    else:
        print("无效的选择")
