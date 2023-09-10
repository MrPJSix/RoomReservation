from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
import datetime

# Create your models here.
""" 用户模型 """


### 用户管理模型
class UserManager(BaseUserManager):
    def create_user(self, user_id, email, user_name="无名用户", password=None):
        if not user_id:
            raise ValueError('User_id must be set!')
        if not email:
            raise ValueError('Email must be set!')

        user = User(
            user_id=user_id,
            user_name=user_name,
            email=email,
        )
        user.set_password(password)
        user.save()
        return user

    # 设管理员账号为admin, 密码123456
    def create_superuser(self, user_id, user_name="administrator", password=None, is_staff=True):
        if not user_id:
            raise ValueError('Users must have an user_id')

        user = User(
            user_id=user_id,
            user_name=user_name,
            is_staff=is_staff,
            is_superuser=True,
        )
        user.set_password(password)
        user.save()
        return user


class User(AbstractBaseUser, PermissionsMixin):
    user_id = models.CharField(max_length=25, primary_key=True, verbose_name=u"用户账号")  # 账号
    user_name = models.CharField(max_length=25, verbose_name=u"用户昵称")  # 姓名/昵称
    email = models.EmailField(unique=True, null=True, verbose_name=u"邮箱")
    credits = models.PositiveIntegerField(default=100, verbose_name=u"信誉值")
    default_times = models.PositiveIntegerField(default=0, verbose_name=u"违约次数")
    is_staff = models.BooleanField(default=False)

    objects = UserManager()
    USERNAME_FIELD = "user_id"
    REQUIRED_FIELDS = ['user_name']

    class Meta:
        db_table = "user_info"
        verbose_name = '用户管理'
        verbose_name_plural = '用户管理'

    def __str__(self):
        return f'User-{self.user_id} : {self.user_name}'


""" 校区模型 """


class Campus(models.Model):
    campus_id = models.CharField(max_length=10, primary_key=True,
                                 verbose_name=u"校区编码")  # 校区编码， 比如campus_name为江湾校区，则可设camapus_id为JW
    campus_name = models.CharField(max_length=25, verbose_name=u"校区")

    class Meta:
        db_table = "campus_info"
        verbose_name = '校区管理'
        verbose_name_plural = '校区管理'

    def __str__(self):
        return f'Campus-{self.campus_id} : {self.campus_name}'


""" 教学楼模型 """


class Building(models.Model):
    building_id = models.CharField(max_length=10, primary_key=True, verbose_name=u"教学楼编码")  # 教学楼编码 JWA
    campus = models.ForeignKey(Campus, on_delete=models.CASCADE, verbose_name=u"校区编码")
    building_name = models.CharField(max_length=25, verbose_name=u"教学楼名称")

    class Meta:
        db_table = "building_info"
        verbose_name = '教学楼管理'
        verbose_name_plural = '教学楼管理'

    def __str__(self):
        return f'Building-{self.building_name} of Campus-{self.campus_id} '


""" 自习室模型 """
STUDYROOM_TYPE = (
    ('1', '教室自习室'),
    ('2', '图书馆自习室'),
    ('3', '其他区域自习室')
)


class Room(models.Model):
    room_id = models.AutoField(primary_key=True, verbose_name=u"自习室ID")  # 插入时自动生成
    building = models.ForeignKey(Building, on_delete=models.CASCADE, verbose_name=u"教学楼编码")
    type = models.CharField(choices=STUDYROOM_TYPE, max_length=1, default='1', verbose_name=u"类型")
    room_name = models.CharField(max_length=25, verbose_name=u"名称")
    number_of_seats = models.PositiveIntegerField(default=0, verbose_name=u"座位数量")
    is_available = models.BooleanField(default=True, verbose_name=u"是否开放")
    open_time = models.TimeField(default=datetime.time(7, 0), verbose_name=u"开放时间")
    close_time = models.TimeField(default=datetime.time(22, 0), verbose_name=u"关闭时间")
    is_allnight = models.BooleanField(default=False, verbose_name=u"是否通宵")
    have_charge = models.PositiveIntegerField(default=0, verbose_name=u"是否有充电设备")

    class Meta:
        db_table = "room_info"
        verbose_name = '自习室管理'
        verbose_name_plural = '自习室管理'

    def __str__(self):
        return f'Room-{self.room_name} of Builind-{self.building_id}'


""" 座位模型 """


class Seat(models.Model):
    seat_id = models.AutoField(primary_key=True, verbose_name=u"座位ID")  # 座位唯一标识，插入时自动生成
    room = models.ForeignKey(Room, on_delete=models.CASCADE, verbose_name=u"自习室ID")
    seat_number = models.CharField(max_length=3, verbose_name=u"座位编号")  # 座位编号，跟seat_id不同 - 1 ~ 50
    can_charge = models.BooleanField(default=False, verbose_name=u"是否可充电")
    QR_Code = models.URLField(max_length=200, blank=True, null=True, verbose_name=u"二维码链接")

    class Meta:
        unique_together = ('room_id', 'seat_number',)
        db_table = "seat_info"
        verbose_name = '座位管理'
        verbose_name_plural = '座位管理'

    def __str__(self):
        return f'Seat-{self.seat_number} of Room-{self.room_id}'


""" 预约模型 """
RESERVATION_STATE = (
    ('0', '未生效'),
    ('1', '已生效'),
    ('2', '已取消'),
    ('3', '已违约'),
    ('4', '已结束')
)
HOURS_CHOICES = (
    (1, '1小时'),
    (2, '2小时'),
    (3, '3小时'),
    (4, '4小时')
)


class Reservation(models.Model):
    reservation_id = models.AutoField(primary_key=True, verbose_name=u"预约记录ID")
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name=u"用户账号")
    room = models.ForeignKey(Room, on_delete=models.DO_NOTHING, verbose_name=u"自习室ID")
    seat = models.ForeignKey(Seat, on_delete=models.DO_NOTHING, verbose_name=u"座位ID")
    date = models.DateField(auto_now_add=True, verbose_name=u"预约日期")
    reservation_time = models.TimeField(verbose_name=u"预约时间")
    reservation_hours = models.IntegerField(choices=HOURS_CHOICES, default=4, verbose_name=u"预约时长")
    reservation_status = models.CharField(choices=RESERVATION_STATE, max_length=1, default='0',
                                          verbose_name=u"预约状态")

    class Meta:
        db_table = "reservation_info"
        verbose_name = '预约记录管理'
        verbose_name_plural = '预约记录管理'

    def __str__(self):
        return f'Reservation {self.reservation_id}'


""" 根据座位的创建和删除来更新对应自习室的座位数量 """


@receiver([post_save, post_delete], sender=Seat)
def update_number_of_seats(sender, instance, **kwargs):
    # 监测每次对座位表的修改，并更新自习室的number_of_seats字段
    room = instance.room
    number_of_seats = Seat.objects.filter(room_id=room.room_id).count()
    room.number_of_seats = number_of_seats
    room.save()


""" 根据座位的创建和删除来更新对应自习室的充电座位数量 """


@receiver([post_save, post_delete], sender=Seat)
def update_have_charge(sender, instance, **kwargs):
    room = instance.room
    charge_seats = Seat.objects.filter(room_id=room.room_id, can_charge=True).count()
    room.have_charge = charge_seats
    room.save()

# """ 根据预约记录更新对应自习室的可用座位数量 """
# @receiver(post_save, sender=Reservation)
# def update_number_of_seats(sender, instance, **kwargs):
#     room = instance.room
#     all_seats_count = Seat.objects.filter(room_id=room.room_id).count()
#     now = datetime.datetime.now()
#
#     seats_reservation = Reservation.objects.filter(
#         date=datetime.date.today(),
#         room=room.room_id,
#         reservation_status__in=('0', '1')
#     )
#
#     unavailable_seats = 0
#     for reservation in seats_reservation:
#         if reservation.reservation_status=='1':
#             unavailable_seats += 1
#         else:
#             hour = now.hour
#             time_now = datetime.time(now.hour, now.minute)
#             start_time = reservation.reservation_time
#             end_time = (datetime.datetime.combine(datetime.datetime.min, start_time) +
#                         reservation.reservation_hours).time()
#
#             flag1 = (reservation.reservation_time.hour - hour <= 1)
#             flag2 = (start_time <= time_now <= end_time)
#             if flag1 or flag2:
#                 unavailable_seats += 1
#     room.number_of_seats = all_seats_count - unavailable_seats
#     room.save()
