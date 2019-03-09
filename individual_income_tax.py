#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys

x=input("请输入您的月薪（元，含五险一金）：")
salary=float(x)

y=input("请输入您的专项扣除总额（元）：")
kouchu=float(y)

#深圳市个税起征点
threshold=5000
#深圳市2018年度职工月平均工资是8348，最低工资2200
average=8348
lowest=2200

if salary<lowest:
	print("低于最低工资标准，请找当地劳动部门仲裁")
	exit()
if salary>=100000000:
	print("地球已经容不下你了，你可以滚到火星去吧")
	exit()
if kouchu>salary:
	print("我只是个小工具，不要这样来测试好吧")
	exit()

#计算缴存基数
cardinal=0
if salary<=lowest:
	cardinal=lowest
elif salary>=average*3:
	cardinal=average*3
else:
	cardinal=salary

#扣除五险一金剩余(按深圳市户籍计算)
#公积金按12%缴交
left=salary-cardinal*(0.08+0.02+0.12)-lowest*0.003

sum_tax=0.0
sum_income=0.0
def calc_income_new(month):
	start_tax=threshold+kouchu
	if left<=start_tax:
		return 0, left
	global sum_tax
	global sum_income
	curr_tax=0.0
	tax_amount=(left-start_tax)*month
	if tax_amount<=36000:
		curr_tax=tax_amount*0.03-0-sum_tax
	elif tax_amount<=144000:
		curr_tax=tax_amount*0.1-2520-sum_tax
	elif tax_amount<=300000:
		curr_tax=tax_amount*0.2-16920-sum_tax
	elif tax_amount<=420000:
		curr_tax=tax_amount*0.25-31920-sum_tax
	elif tax_amount<=660000:
		curr_tax=tax_amount*0.3-52920-sum_tax
	elif tax_amount<=960000:
		curr_tax=tax_amount*0.35-85920-sum_tax
	else:
		curr_tax=tax_amount*0.45-181920-sum_tax

	curr_income=left-curr_tax
	sum_tax+=curr_tax
	sum_income+=curr_income

	return curr_tax, curr_income

def calc_income():
	if left<=threshold:
		return 0, left
	curr_tax=0.0
	tax_amount=left-threshold
	if tax_amount<=3000:
		curr_tax=tax_amount*0.03-0
	elif tax_amount<=12000:
		curr_tax=tax_amount*0.1-210
	elif tax_amount<=25000:
		curr_tax=tax_amount*0.2-1410
	elif tax_amount<=35000:
		curr_tax=tax_amount*0.25-2660
	elif tax_amount<=55000:
		curr_tax=tax_amount*0.3-4410
	elif tax_amount<=80000:
		curr_tax=tax_amount*0.35-7160
	else:
		curr_tax=tax_amount*0.45-15160
	
	curr_income=left-curr_tax

	return curr_tax, curr_income

if __name__ == '__main__':
#	print(salary)
#	print(kouchu)
#	print(cardinal)
#	print(left)
#	(curr_tax, curr_income) = calc_income(1);
#	print(curr_tax)
#	print(curr_income)

	print("\n新税法：")
	print("----------------------------------------")
	print("|\t|月纳税额\t|到手收入\t|")
	print("----------------------------------------")
	for month in range(1, 13):
		(curr_tax, curr_income)=calc_income_new(month)
		print("|%d月\t|%.2f\t|%.2f\t|" % (month, curr_tax, curr_income))
		print("----------------------------------------")
	print("|总计\t|%.2f\t|%.2f\t|" % (sum_tax, sum_income))
	print("----------------------------------------")

	print("\n旧税法：")
	(old_tax, old_income)=calc_income()
	print("月度交税：%.2f，年度交税：%.2f" % (old_tax, old_tax * 12))
	print("年度到手收入：%.2f" % (old_income * 12))
	print("\n")
	
