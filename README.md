# Bank Mobile Application

This is a test **bank mobile application** that works offline

---
### problems

1. change password: new hash passwrd save wrongly and you can't access that and your account
2. if you want to pay installment in day more than 1, see raise error in database, but app run corrently
3. if you enter date in wrong format, see raise error in database, but app run corrently
4. you can give loan and have transaction and pay installment with block account(show transaction successfully to user, but didn't do in database)
5. add loan score after give money(why?), so it's not min money in last two month for loan score
6. don't show sum_of_pay and sum_of_unpaid for installments to admin(for user show corrently)

---
### weaknesses

1. GUI is not good
2. project does not have email for actions
3. project does not have dynamic password by number or email
4. project does not have injection sql
