# Generated by Django 5.0.2 on 2024-03-10 05:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ledger', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ledger',
            name='receipt_disbursement',
            field=models.CharField(choices=[('receipt', '收入'), ('disbursement', '支出'), ('ignore', '不计收支')], max_length=255, verbose_name='收/支'),
        ),
        migrations.AlterField(
            model_name='ledger',
            name='transaction_category',
            field=models.CharField(choices=[('Cultural Leisure ', ' 文化休闲'), ('Investment and Wealth Management ', '投资理财'), ('Catering Cuisine ', '餐饮美食'), ('Recharge Payment ', '充值缴费'), ('Revenue ', '收入'), ('Home Furnishing ', '家居家装'), ('Credit Borrowing and Repayment ', '信用借还'), ('Transfer Red Envelope ', '转账红包'), ('Refund ', '退款'), ('Hotel tourism ', '酒店旅游'), ('Dress up ', '服饰装扮'), ('Life Services', '生活服务'), ('Public Service ', '公共服务'), ('Medical Health ', '医疗健康'), ('Account Access', '账户存取'), ('Beauty and hairdressing ', '美容美发'), ('Transportation Travel ', '交通出行'), ('Business Services', '商业服务'), ('Mother Infant Parent Child ', '母婴亲子'), ('Sports Outdoor ', '运动户外'), ('Pet ', '宠物'), ('Daily necessities', '日用百货'), ('Digital Appliances', '数码电器'), ('Love car maintenance ', '爱车养车'), ('Other ', '其他')], max_length=255, verbose_name='交易分类'),
        ),
        migrations.AlterField(
            model_name='ledger',
            name='transaction_status',
            field=models.CharField(choices=[('transaction_successful', '交易成功'), ('transaction_closed', '交易关闭'), ('thawing_successful', '解冻成功'), ('refund_successful', '退款成功'), ('payment_successful', '支付成功')], max_length=255, verbose_name='交易状态'),
        ),
    ]