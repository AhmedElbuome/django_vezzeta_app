from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import gettext_lazy as _
from django.db.models.signals import post_save
from django.utils.text import slugify

def image_upload(instance, filename):
    
    imagename , extension = filename.split('.') 

    return 'profile/%s.%s'%(instance.id, extension)

GENDER = (
    ('M', 'Male'),
    ('F', 'Female')
)
class Profile(models.Model):
    """Model definition for Profile."""

    DOCTOR_IN = (
        ('الجلدية','الجلدية'),
        ('أسنان','أسنان'),
        ('نفسي','نفسي'),
        ('اطفال حديثي الولادة','اطفال حديثي الولادة'),
        ('نساء و توليد','نساء و توليد'),
        
    )
    
    user                 = models.OneToOneField(User, verbose_name=_("user"), on_delete=models.CASCADE)
    name                 = models.CharField(_("الاسم :"), max_length=50)
    who_i                = models.TextField(_("من انا :"), max_length=1000)
    price                = models.IntegerField(_("سعر الكشف :"), blank=True, null=True)
    image                = models.ImageField(_("الصورة الشخصية :"), upload_to=image_upload, blank=True, null=True)
    subtitle             = models.CharField(_("نبذه عنك"), max_length=50)
    address              = models.CharField(_("المحافظة :"), max_length=50)
    address_detail       = models.CharField(_("العنوان بالتفصيل :"), max_length=50)
    number_phone         = models.CharField(_("رقم التلفون"), max_length=50)
    working_hours        = models.CharField(_("عدد ساعات العمل :"), max_length=50)
    join_new             = models.DateTimeField(_("وقت الانضمام"),auto_now_add=True, blank=True, null=True)
    gender               = models.CharField(_("النوع :"), choices=GENDER, max_length=50)
    waiting_hours        = models.IntegerField(_("مدة الانتظار :"))
    facebook             = models.CharField( max_length=50, blank=True, null=True)
    instgram             = models.CharField( max_length=50, blank=True, null=True)
    google               = models.CharField( max_length=50, blank=True, null=True)
    doctor               = models.CharField(_("دكتور ؟"),choices=DOCTOR_IN, max_length=50, blank=True, null=True)
    specialist_doctor    = models.CharField(_("متخصص في ؟"), max_length=50)
    slug                 = models.SlugField(_("slug"), blank=True, null=True)

    def save(self, *args, **kwargs):
        
        if not self.slug:
            self.slug = slugify(self.user.username)
        
        super(Profile, self).save(*args, **kwargs) # Call the real save() method

    class Meta:
        """Meta definition for Profile."""

        verbose_name = _('Profile')
        verbose_name_plural = _('Profiles')

    def __str__(self):
        """Unicode representation of Profile."""
        return str(self.user.username)

def create_profile(sender, **kwargs):
    
    if kwargs['created']:
        
        Profile.objects.create(user = kwargs['instance'])
        
post_save.connect(create_profile, sender=User)
