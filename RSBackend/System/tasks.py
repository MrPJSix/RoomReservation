from datetime import datetime, timedelta
from apscheduler.schedulers.background import BackgroundScheduler
from django.core.mail import send_mail
from django_apscheduler.jobstores import DjangoJobStore
from Model.models import Reservation
from RSBackend import settings
from pytz import timezone

# 处理学生违约函数
def handle_reservation_default(reservation_id):
    try:
        reservation = Reservation.objects.get(reservation_id=reservation_id)
        if reservation.reservation_status == '0':
            user = reservation.user
            user.default_times += 1
            user.credits -= 10
            user.save()
            reservation.reservation_status = '3'
            reservation.save()
            print(f"{user.user_name}已经违约！")
            # 定时发送邮件提醒
            subject = '自习室预约签到失败'
            message = f"{reservation.user.user_name}您在{reservation.reservation_time}的预约签到失败，预约违约！"
            # recp = '1395440228@qq.com'
            recp = reservation.user.email
            result = send_mail(subject=subject, message=message, from_email=settings.EMAIL_HOST_USER,
                               recipient_list=[recp, ])
            print(result)

    except Reservation.DoesNotExist:
        print("预约记录未找到")


# 处理签到提醒
def handle_reservation_sign(reservation_id, hint):
    try:
        reservation = Reservation.objects.get(reservation_id=reservation_id)
        if reservation.reservation_status == '0':
            user = reservation.user
            # 定时发送邮件提醒
            subject = '自习室签到提醒'
            if hint > 0:
                message = f"{reservation.user.user_name}您在{reservation.reservation_time}的已预定座位，请准时签到！"
            else:
                message = f'{reservation.user.user_name}您在{reservation.reservation_time}的已预定座位，您还未签到，请及时签到！'
            # recp = '1395440228@qq.com'
            recp = reservation.user.email
            result = send_mail(subject=subject, message=message, from_email=settings.EMAIL_HOST_USER,
                               recipient_list=[recp, ])
            print(result)

    except Reservation.DoesNotExist:
        print("预约记录未找到")


def hand_reservation_end(reservation_id):
    try:
        reservation = Reservation.objects.get(reservation_id=reservation_id)
        reservation.reservation_status = '4'
        reservation.save()
        print(f"{reservation.user.user_name}预约已结束！")
    except Reservation.DoesNotExist:
        print("预约记录未找到")


def create_reservation_task(reservation):
    tz = timezone('Asia/Shanghai')

    scheduler = BackgroundScheduler()
    scheduler.add_jobstore(DjangoJobStore(), 'reservation')

    res_hour = reservation.reservation_time.hour
    now = datetime.now()
    if reservation.reservation_status == '0':
        if res_hour == now.hour:
            default_time = datetime.combine(reservation.date, reservation.reservation_time) + \
                           timedelta(minutes=now.minute + 5)
            scheduler.add_job(
                handle_reservation_default,
                'date',
                run_date=default_time,
                args=[reservation.reservation_id],
                id=str(reservation.reservation_id)+'_1',
                name=f'{reservation.user.user_id}的预约违约任务',
                replace_existing=True,
                timezone=tz,
            )
        else:
            default_time = datetime.combine(reservation.date, reservation.reservation_time) + \
                           timedelta(minutes=15)
            # 学生15分钟内未签到违约定时任务
            scheduler.add_job(
                handle_reservation_default,
                'date',
                run_date=default_time,
                args=[reservation.reservation_id],
                id=str(reservation.reservation_id)+'_2',
                name=f'{reservation.user.user_id}的预约违约任务',
                replace_existing=True,
                timezone=tz,
            )
            print("添加{reservation.user.user_id}的预约违约处理任务")
        
            default_time = datetime.combine(reservation.date, reservation.reservation_time) - timedelta(minutes=15)
            # 学生预约前15min自动邮件提醒
            scheduler.add_job(
                handle_reservation_sign,
                'date',
                run_date=default_time,
                args=[reservation.reservation_id, 1],
                id=str(reservation.reservation_id)+'_3',
                name=f'{reservation.user.user_id}的预约前15分钟签到提醒任务',
                replace_existing=True,
                timezone=tz,
            )
            print("添加{reservation.user.user_id}的预约前15分钟提醒任务")
            default_time = datetime.combine(reservation.date, reservation.reservation_time) + timedelta(minutes=10)
            # 学生预约后10min自动邮件提醒
            scheduler.add_job(
                handle_reservation_sign,
                'date',
                run_date=default_time,
                args=[reservation.reservation_id, -1],
                id=str(reservation.reservation_id)+'_4',
                name=f'{reservation.user.user_id}的预约后10分钟签到提醒任务',
                replace_existing=True,
                timezone=tz,
            )
            print("添加{reservation.user.user_id}的预约后10分钟提醒任务")
        
    elif reservation.reservation_status == '1':
        end_time = datetime.combine(reservation.date, reservation.reservation_time) + timedelta(
            hours=reservation.reservation_hours)
        # 预约时长结束后，结束该条预约记录
        scheduler.add_job(
            hand_reservation_end,
            'date',
            run_date=end_time,
            args=[reservation.reservation_id],
            id=str(reservation.reservation_id)+'_5',
            name=f'{reservation.user.user_id}的自动结束预约任务',
            replace_existing=True,
            timezone=tz,
        )
        print("添加{reservation.user.user_id}的自动结束预约任务")

    scheduler.start()

    jobs = scheduler.get_jobs()
    for job in jobs:
        print(f'ID: {job.id}, Name: {job.name}, Next run: {job.next_run_time}')