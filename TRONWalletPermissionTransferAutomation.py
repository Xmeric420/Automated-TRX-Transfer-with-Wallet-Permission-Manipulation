from tronpy import Tron
from tronpy.keys import PrivateKey
import time
import os

# 初始化Tron客户端
client = Tron()

# 输入A钱包公钥和B钱包公钥、私钥
print (f"Tron链骗取gas自动转TRX程序")
print (f"赞助(Tron链)TUEvQhBgy7WQujayBbKgRc2c7PPW7hvXbs")
print (f"")
print (f"")
print (f"")
wallet_address_a = input("请输入A钱包公钥(没有权限转账的钱包)：")
wallet_address_b = input("请输入B钱包公钥(拥有A钱包的转账权限)：")
private_key_b_str = input("请输入B钱包私钥(拥有A钱包的转账权限)：")

# 输入阈值、手续费和检测频率
threshold_trx = float(input("请输入转账阈值（钱包里的TRX达到多少转多少，默认15）：") or 15)
fee_trx = float(input("请输入预留手续费（TRX，默认0.5）：") or 0.5) 
check_frequency = int(input("请输入检测频率（单位为秒，默认10秒）：") or 10)

# 创建B钱包私钥对象
private_key_b = PrivateKey(bytes.fromhex(private_key_b_str))

# 获取A钱包余额
def check_balance(wallet_address):
    account = client.get_account(wallet_address)
    balance = account.get('balance', 0)  # 获取余额，单位是微TRX
    return balance / 1_000_000  # 转换为TRX

# 转账函数
def transfer_trx():
    balance_a = check_balance(wallet_address_a)
    print(f"A钱包余额: {balance_a:.6f} TRX")

    # 如果A钱包余额大于设定的阈值和手续费后余额足够，则执行转账
    if balance_a >= (threshold_trx + fee_trx):
        print(f"A钱包余额达到{threshold_trx} TRX，开始转账...")

        # 计算实际转账金额，扣除手续费
        amount_trx = (balance_a - fee_trx)

        # 构建转账交易
        txn = (
            client.trx.transfer(wallet_address_a, wallet_address_b, int(amount_trx * 1_000_000))  # 转账金额
            .build()
            .sign(private_key_b)  # 用B钱包私钥签署交易
        )

        try:
            # 广播交易并获取交易ID
            result = txn.broadcast()

            if 'result' in result and result['result'] == True:
                print(f"Transaction successful! Transaction ID: {result['txid']}")
            else:
                print(f"Transaction failed! Error: {result.get('message', 'Unknown error')}")

        except Exception as e:
            print(f"An error occurred: {str(e)}")
    else:
        print(f"余额小于阈值，当前余额: {balance_a:.6f} TRX")
        print(f"{check_frequency}秒后进行下一次检测")

# 清屏函数，模拟cmd的cls命令
def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

# 进入检测和转账循环
while True:
    clear_screen()  # 每次循环清屏，模拟cmd的效果
    transfer_trx()
    time.sleep(check_frequency)  # 根据用户设定的频率每隔一定时间检测一次
