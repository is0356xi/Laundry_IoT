import time
import pigpio

def StartLaundry():
    servoPush()
    time.sleep(SERVO_TIME)
    servoRelease()

def calcServoDuty(ratio):   # ratio:0-1でサーボ角度を指定
    # SG92Rの制御パルスが0.5ms-2.4msなのでdutyに25000(1000000/20*0.5)-120000(100000/20*2.4)をマッピングする
    duty = 25000 + (120000 - 25000) * ratio
    return duty

def moveServo(ratio):
    duty = calcServoDuty(ratio)
    pi.hardware_PWM(PORT_PWM, SERVO_PERIOD, int(duty))

def servoRelease():
    moveServo(SERVO_RELEASE)

def servoPush():
    moveServo(SERVO_PUSH)

if __name__=='__main__':
    # サーボのPWMパラメータ
    SERVO_RELEASE = 0.5 # ボタン解放状態（サーボモータ角度中間）
    SERVO_PUSH = 0.20   # ボタン押下状態
    SERVO_TIME = 1    # サーボモータを押す時間[秒]
    
    pi = pigpio.pi()
    
    # servo setting
    PORT_PWM = 18
    SERVO_PERIOD = 50   # [Hz] :PWMサイクル20ms
    pi.set_mode(PORT_PWM, pigpio.OUTPUT)
    moveServo(0.5)
    
    
    StartLaundry()