create DATABASE IF NOT EXISTS bank;
USE bank;

CREATE TABLE IF NOT EXISTS user
(
    user_id INT PRIMARY KEY AUTO_INCREMENT,
    user_name varchar(50) NOT NULL UNIQUE ,
    first_name varchar(50) NOT NULL,
    last_name varchar(50) NOT NULL,
    password varchar(1000) NOT NULL,
    is_admin TINYINT(1) default 0,
    email varchar(256) unique ,
    phone_number varchar(11) unique
);

CREATE TABLE IF NOT EXISTS account
(
    user_id int NOT NULL,
    account_number INT PRIMARY KEY AUTO_INCREMENT,
    is_active tinyint(1) default 1,
    start_date DATE NOT NULL DEFAULT (CURRENT_DATE),
    balance int default 100000,
    active_loan_id int default NULL,
    deactivation_date DATE default NULL,
    deactivation_reason varchar(256) default NULL,
    foreign key (user_id) references User(user_id)
);

CREATE TABLE IF NOT EXISTS transaction
(
    user_id int,
    source_account_number int,
    destination_account_number int,
    source_account_balance_after_transaction int,
    destination_account_balance_after_transaction int,
    date datetime not null default (now()),
    amount int,
    primary key (user_id,destination_account_number,source_account_number,date),
    foreign key (user_id) references user(user_id),
    foreign key (destination_account_number) references Account(account_number),
    foreign key (source_account_number) references Account(account_number)
);

CREATE TABLE IF NOT EXISTS loan
(
    loan_id INT PRIMARY KEY AUTO_INCREMENT,
    is_active TINYINT(1) default 1,
    amount int NOT NULL,
    user_id int,
    account_number int,
    installment_count int NOT NULL,
    installment_paid int NOT NULL default 0,
    date date not null default (curdate()),
    foreign key (user_id) references User(user_id),
    foreign key (account_number) references Account(account_number)
);

start transaction ;
    insert into user (user_name,first_name,last_name,password,email,phone_number)
    values ('admin','admin','admin','4eb334944825e750d5e62706ddb02c4b7c567596319a0bb3ba3ededd74f4b3ff','admin@gmail.com','09011111111');
commit;

CREATE TABLE IF NOT EXISTS installment
(
    loan_id int,
    user_id int,
    account_number int,
    pay_date date not null ,
    is_paid TINYINT(1) default 0,
    amount int,
    primary key (loan_id,pay_date),
    foreign key (user_id) references user(user_id),
    foreign key (account_number) references account(account_number),
    foreign key (loan_id) references loan(loan_id)
);

create function check_email
(
    input_email CHAR(255)
)
    returns bool
    deterministic
begin
    declare x bool;
    if input_email like "%@%.%"
        then
        set x := true;
    else
        set x := false;
    end if;
    return x;
end;

create function check_password
(
    input_user_id int,
    input_password CHAR(255)

)
    returns bool
    deterministic
begin
    declare x bool;
    if (select password
        from user u
        where u.user_id = input_user_id) = input_password
        then
        set x := true;
    else
        set x := false;
    end if;
    return x;

end;



create function check_phone_number
(
    input_phone_number CHAR(11)
)
    returns bool
    deterministic
begin
    declare x bool;
    if (input_phone_number REGEXP '^[0-9]+$' and length(input_phone_number) = 11)
        then
        set x := true;
    else
        set x := false;
    end if;
    return x;
end;


create function check_username
(
    input_user_name CHAR(50)
)
    returns bool
    deterministic
begin
    declare x bool;
    if (select count(*)
        from user
        where user_name = input_user_name) > 0
        then
        set x := false;
    else
        set x := true;
    end if;
    return x;
end;


create function check_account_number
(
    input_account_number int
)
    returns bool
    deterministic
begin
    declare x bool;
    if (select count(*)
        from account
        where account_number = input_account_number) > 0
        then
        set x := true;
    else
        set x := false;
    end if;
    return x;

end;


create function signup
(
    input_first_name CHAR(50),
    input_last_name CHAR(50),
    input_password CHAR(255),
    input_user_name CHAR(50),
    input_email CHAR(255),
    input_phone_number CHAR(11)
)
    returns int
    deterministic
begin
    declare x int;
    declare y int;
    select count(*) into y
    from user
    where user_name = input_user_name or email = input_email or phone_number = input_phone_number;
    if y > 0
        then
        set x := 0;
    else
        insert into user(first_name,last_name,password,user_name,email,phone_number)
        values (input_first_name,input_last_name,input_password,input_user_name,input_email,input_phone_number);
        select user_id
        into x
        from User
        where input_user_name = user_name;
    end if;
    return x;
end;


delimiter //
create procedure all_users
()
begin
    select user_name, first_name, last_name, email, phone_number
    from User;
end//;
delimiter ;
call all_users();
drop procedure all_users;

create function make_admin
(
    input_user_id int,
    input_user_name char(50)
)
    returns bool
    deterministic
begin
    declare x bool;
    if (select is_admin
        from user u
        where u.user_id = input_user_id) = 1
        then
        update user
            set is_admin = 1
        where user_name = input_user_name;
        set x := true;
    else
        set x:=false;
    end if;
    return x;
end;


create function is_admin
(
    input_user_id int
)
    returns bool
    deterministic
begin
    declare x bool;
    if (select is_admin
        from user u
        where u.user_id = input_user_id) = 1
        then
        set x := true;
    else
        set x := false;
    end if;
    return x;
end;


CREATE function login
(
    input_username CHAR(50),
    input_password CHAR(255)
)
    returns int
    deterministic
BEGIN
    declare x int;
    select u.user_id
    into x
    from User u
    WHERE u.password= input_password and
               u.user_name=input_username;
    return x;
END;

create function change_password
(
    input_user_id int,
    input_password char(255),
    new_password char(255)
)
    returns bool
    deterministic
begin
    declare x bool;
    if (select password
        from User u
        where u.user_id = input_user_id) = input_password
        then
        update user
            set password = new_password
        where user_id = input_user_id;
        set x := true;
    else
        set x := false;
    end if;
    return x;
end;


create function add_admin
(
    input_user_id int,
    input_user_id_to_be_admin int
)
    returns int
    deterministic
begin
    declare x int;
    if (select is_admin
        from user u
        where u.user_id = input_user_id) = 1
        then
        update user
            set is_admin = 1
        where user_id = input_user_id_to_be_admin;
        select user_id
        into x
        from user
        where user_id = input_user_id_to_be_admin;
    else
        set x := 0;
    end if;
    return x;
end;


create function check_loan_number
(
    input_user_id int,
    input_loan_id int
)
    returns bool
    deterministic
begin
    declare x bool;
    if (select count(*)
        from Loan L
        where L.loan_id = input_loan_id and
              (L.user_id = input_user_id or (select is_admin
                                             from user
                                             where user.user_id = input_user_id)=1)) > 0
        then
        set x := true;
    else
        set x := false;
    end if;
    return x;
end;

create function sum_of_paid
(
    input_user_id int,
    input_loan_id int
)
    returns int
    deterministic
begin
    declare x int;
    select sum(amount)
    into x
    from installment
    where loan_id = input_loan_id and
          user_id = input_user_id and
          is_paid = 1;
    return x;
end;

create function not_paid
(
    input_user_id int,
    input_loan_id int
)
    returns int
    deterministic
begin
    declare x int;
    select sum(amount)
    into x
    from installment
    where loan_id = input_loan_id and
          user_id = input_user_id and
          is_paid = 0;
    return x;
end;

create function state_loan
(
    input_user_id int,
    input_loan_id int
)
    returns bool
    deterministic
begin
    declare x bool;
    if (select is_admin from user where user_id = input_user_id) = 1 or (select count(*)
        from Loan L
        where L.loan_id = input_loan_id and
              L.user_id = input_user_id and
              L.is_active = 1) > 0
        then
        if (select is_active from Loan where loan_id = input_loan_id) = 1
            then
            set x := true;
        else
            set x := false;
        end if;
    else
        set x := false;
    end if;
    return x;

end;

create function get_id
(
    input_user_id int,
    input_user_name char(50)
)
    returns int
    deterministic
begin
    declare x int;
    select user_id
    into x
    from user
    where user_name = input_user_name and
          (user_id = input_user_id or (select is_admin
                                       from user
                                       where user.user_id = input_user_id)=1);
    return x;
end;

delimiter //
create procedure get_users_info
(
    input_user_id int
)
begin
    if (select is_admin
        from user u
        where u.user_id = input_user_id) = 1
        then
        select user_name, first_name, last_name, email, phone_number
        from User;
    else
        select "You are not allowed to see this information";
    end if;
end//;
delimiter ;


create function get_email
(
    input_user_id int
)
    returns varchar(256)
    deterministic
begin
    declare x varchar(256);
    select email
    into x
    from User
    where user_id = input_user_id;
    return x;
end;

create function add_account
(
    input_admin_id int,
    input_user_id int
)
    returns int
    deterministic
begin
    declare x int;
    if (select is_admin
        from user u
        where u.user_id = input_admin_id) = 1
        then
        insert into account(user_id)
        values (input_user_id);
        select account_number
        into x
        from account
        where user_id = input_user_id
        order by account_number desc
        limit 1;
    else
        set x := 0;
    end if;
    return x;
end;

delimiter //
create procedure all_accounts
(
    input_user_id int
)
begin

    select A.account_number,A.start_date,A.balance,A.active_loan_id,A.deactivation_date,A.deactivation_reason
    from User U
    join Account A on U.user_id = A.user_id
    where U.user_id = input_user_id;
end//;
delimiter ;

drop procedure all_accounts;
call all_accounts(4);

DELIMITER //
create procedure get_recent_transaction
(
    input_user_id int,
    input_account_number int,
    input_number int
)
begin
    if (select is_admin
        from user u
        where u.user_id = input_user_id) = 1
        then
        select source_account_number, destination_account_number, amount,  date
        from Transaction
        where source_account_number = input_account_number
        or destination_account_number = input_account_number
        ORDER BY date DESC
        limit input_number;
    elseif (select is_account_for_user(input_account_number,input_user_id) = 1)
        then
        select source_account_number, destination_account_number, amount,  date
        from Transaction
        where (source_account_number = input_account_number
        or destination_account_number = input_account_number)
        ORDER BY date DESC
        limit input_number;
    else
        select "You are not allowed to see this information";
    end if;
end//;
delimiter ;

delimiter //
create procedure get_period_transaction
(
    input_user_id int,
    input_account_number int,
    input_starting_date date,
    input_ending_date date
)
begin
    if (select is_admin
        from user u
        where u.user_id = input_user_id) = 1
        then
        select source_account_number, destination_account_number, amount,  date
        from Transaction
        where date >= input_starting_date
        and date <= input_ending_date
        and (source_account_number = input_account_number or destination_account_number = input_account_number)
        ORDER BY date DESC;
    elseif (select is_account_for_user(input_account_number,input_user_id) = 1)
        then
        select source_account_number, destination_account_number, amount,  date
        from Transaction
        where (source_account_number = input_account_number
        or destination_account_number = input_account_number)
        and date >= input_starting_date
        and date <= input_ending_date
        ORDER BY date DESC;
    else
        select "You are not allowed to see this information";
    end if;
end//;

delimiter ;


delimiter //
create procedure account_info
(
    input_user_id int,
    input_account_number int
)
begin
    select A.account_number,U.first_name, U.last_name, U.email, U.phone_number ,A.start_date, A.balance,A.active_loan_id,A.deactivation_date,A.deactivation_reason
    from Account A
    join User U on A.user_id = U.user_id
    where A.account_number = input_account_number and
          (A.user_id = input_user_id or (select is_admin
                                         from user u
                                         where u.user_id = input_user_id)=1);
end//;
delimiter ;

create function get_first_name
(
    input_user_id int
)
    returns varchar(50)
    deterministic
begin
   declare x varchar(50);
        select first_name
        into x
        from User
        where user_id = input_user_id;
        return x;
end;


create function get_full_name
(
    input_account_number int
)
    returns varchar(50)
    deterministic
begin
    declare x varchar(50);
    select concat(U.first_name,' ',U.last_name)
    into x
    from Account A
    join User U on A.user_id = U.user_id
    where A.account_number = input_account_number;
    return x;

end;

create function is_account_for_user
(
    input_account_number int,
    input_user_id int
)
    returns bool
    deterministic
begin
    declare x bool;
    if (select count(*)
        from Account A
        where A.account_number = input_account_number and
              A.user_id = input_user_id) > 0
        then
        set x := true;
    else
        set x := false;
    end if;
    return x;
end;


create function check_block_account
(
    input_user_id int,
    input_account_number int
)
    returns bool
    deterministic
begin
    declare x bool;
    if (select is_active
        from Account A
        where A.account_number = input_account_number and
              A.user_id = input_user_id) = 1
        then
        set x := true;
    elseif (select is_admin
        from user u
        where u.user_id = input_user_id)=1 and
        (select is_active
        from Account A
        where A.account_number = input_account_number) = 1
        then
        set x := true;
    else
        set x := false;
    end if;
    return x;
end;


create function check_amount
(
    input_amount int,
    input_user_id int,
    input_account_number int
)
    returns bool
    deterministic
begin
    declare x bool;
    if (select balance
        from Account A
        where A.account_number = input_account_number and
              A.user_id = input_user_id) >= input_amount
        then
        set x := true;
    else
        set x := false;
    end if;
    return x;
end;

create function block_account
(
    input_user_id int,
    input_account_number int,
    input_reason varchar(256)
)
    returns bool
    deterministic
begin
    declare x bool;
    if (select is_active
        from Account A
        where A.account_number = input_account_number and
              (A.user_id = input_user_id or
               (select is_admin
                from user u
                where u.user_id = input_user_id)=1)) = 1
        then
        update Account
            set is_active = 0,
                deactivation_date = NOW(),
                deactivation_reason = input_reason
        where account_number = input_account_number;
        if (select check_account_number(input_account_number) )= 1
            then
            set x := true;
        else
            set x := false;
        end if;
    else
        set x := false;
    end if;
    return x;
end;


delimiter //
create procedure money_transfer

(
    input_user_id int,
    input_source_account_number int,
    input_destination_account_number int,
    input_amount int
)
    deterministic
begin
    declare x bool;
    declare sender_balance int;
    declare receiver_balance int;
    declare sender_user_id int;
    select A.user_id
    into sender_user_id
    from Account A
    where A.account_number = input_source_account_number and
          A.is_active = 1;
    select A.balance
    into sender_balance
    from Account A
    where A.account_number = input_source_account_number and
          A.is_active = 1;
    select A.balance
    into receiver_balance
    from Account A
    where A.account_number = input_destination_account_number and
          A.is_active = 1;
    if (select is_account_for_user(input_source_account_number,input_user_id) = 1 or (select is_admin
                                                                                     from user u
                                                                                     where u.user_id = input_user_id)=1)
        then
        if sender_balance >= input_amount
            then
            start transaction;
            update Account
                set balance = sender_balance - input_amount
            where account_number = input_source_account_number;
            update Account
                set balance = receiver_balance + input_amount
            where account_number = input_destination_account_number;
            insert into Transaction(user_id,source_account_number,destination_account_number,amount,source_account_balance_after_transaction,destination_account_balance_after_transaction)
            values (sender_user_id,input_source_account_number,input_destination_account_number,input_amount,sender_balance - input_amount,receiver_balance + input_amount);
            commit;
            set x := true;
        else
            set x := false;
        end if;
    else
        set x := false;
    end if;
    select x;
end;
delimiter ;

create function check_loan_amount
(

    input_user_id int,
    input_account_number int,
    input_amount int
)
    returns bool
    deterministic
begin
    declare x bool;
    if (select loan_score_calculation(input_user_id,input_account_number) >= input_amount)
        then
        set x := true;
    else
        set x := false;
    end if;
    return x;

end;

create function loan_score_calculation
(
    input_user_id int,
    input_account_number int
)
    returns int
    deterministic
begin
    declare x int;
    declare y int;
    declare z int;
    if (select is_admin
        from user u
        where u.user_id = input_user_id) = 1 or (select is_account_for_user(input_account_number,input_user_id) = 1)
        and (select is_active
             from Account A
             where A.account_number = input_account_number) = 1
    then
        select source_account_balance_after_transaction
        into y
        from Transaction
        where source_account_number = input_account_number
        and date < NOW() and date > NOW() - interval 2 month
        order by source_account_balance_after_transaction asc
        limit 1;
        IF y is null
            then
            set y := 0;
        end if;
        select destination_account_balance_after_transaction
        into z
        from Transaction
        where destination_account_number = input_account_number
        and date < NOW() and date > NOW() - interval 2 month
        order by destination_account_balance_after_transaction asc
        limit 1;
        if (y < z and y != 0) or z is null
            then
            set x := y;
        else
            set x := z;
        end if;
    else set x := 0;
    end if;
    return x;
end;

create function loan_application
(
    input_user_id int,
    input_account_number int,
    input_amount int,
    input_mode int
)
    returns bool
    deterministic
begin
    declare x bool;
    declare v_amount int;
    declare v_user_id int;
    declare v_loan_id int;
    declare percent int;
    declare monthly_amount int;
    declare v_installment_count int;
    select A.user_id
    into v_user_id
    from Account A
    where A.account_number = input_account_number;
    select loan_score_calculation(input_user_id,input_account_number)
    into v_amount;
    if ((select count(*)
            from account A
            join bank.user u on A.user_id = u.user_id
            where A.user_id = input_user_id and (A.account_number = input_account_number or
                  u.is_admin = 1) >0))
        then
        if input_amount <= v_amount
            then
            if ((select count(*)
                from Loan L
                where L.account_number = input_account_number and L.is_active = 1) = 0)
                then
                if v_amount > 0
                    then
                    if input_mode = 1
                        then
                        select 15
                        into percent;
                        select 6
                        into v_installment_count;
                    elseif input_mode = 2
                        then
                        select 20
                        into percent;
                        select 12
                        into v_installment_count;
                    elseif input_mode = 3
                        then
                        select 25
                        into percent;
                        select 18
                        into v_installment_count;
                    else
                        set x := false;
                    end if;
                    insert into Loan(amount,user_id,account_number,installment_count)
                    values (input_amount,v_user_id,input_account_number,v_installment_count);
                    select loan_id
                    into v_loan_id
                    from Loan
                    where account_number = input_account_number
                    order by date desc
                    limit 1;
                    set x := true;
                    set monthly_amount := input_amount * (percent+100)/ 100 /v_installment_count;
                    while v_installment_count > 0
                        do
                        insert into installment(loan_id,user_id,account_number,pay_date,is_paid,amount)
                        values (v_loan_id,v_user_id,input_account_number,DATE_ADD(NOW(),INTERVAL v_installment_count MONTH),0,monthly_amount);
                        set v_installment_count := v_installment_count - 1;
                    end while;
                    update Account
                        set active_loan_id = v_loan_id
                    where account_number = input_account_number;
                    update Account
                        set balance = balance + v_amount
                    where account_number = input_account_number;
                else
                    set x := false;
                end if;
            else set x := false;
            end if;
        else
            set x := false;
        end if;
    else
        set x := false;
    end if;
    return x;
end;

delimiter //


create procedure get_loans
(
    input_user_id int
)
begin
    select l.loan_id,L.amount, L.date, L.installment_count, L.installment_paid, L.is_active
    from Loan L
    where L.user_id = input_user_id;
end//;
delimiter ;

create function has_loan
(
    input_user_id int,
    input_account_number int
)
    returns bool
    deterministic
begin
    declare x bool;
    if (select count(*)
        from Loan L
        where (L.user_id = input_user_id or (select is_admin
                                            from user
                                            where user.user_id = input_user_id)=1) and
              L.account_number = input_account_number and
              L.is_active = 1) > 0
        then
        set x := true;
    else
        set x := false;
    end if;
    return x;
end;

delimiter //
create procedure list_of_installment
(
    input_user_id int,
    input_loan_id int
)
begin
    select I.is_paid, I.amount,I.pay_date
    from installment I
    where I.loan_id = input_loan_id and
          (I.user_id = input_user_id or (select is_admin
                                         from user
                                         where user.user_id = input_user_id)=1);
end//;

delimiter ;

create function pay_installment
(
    input_user_id int,
    input_loan_id int
)
    returns bool
    deterministic
begin
    declare x bool;
    declare v_user_id int;
    declare v_account_number int;
    declare v_amount int;
    declare v_is_loan_active int;
    declare v_date_to_pay date;
    declare v_number_of_installment_left int;
    select installment_count - installment_paid
    into v_number_of_installment_left
    from Loan
    where loan_id = input_loan_id;
    select user_id
    into v_user_id
    from Loan
    where loan_id = input_loan_id
    limit 1;
    select account_number
    into v_account_number
    from Loan
    where loan_id = input_loan_id
    limit 1;
    select amount
    into v_amount
    from installment
    where loan_id = input_loan_id
    order by pay_date asc
    limit 1;
    select is_active
    into v_is_loan_active
    from Loan
    where loan_id = input_loan_id
    limit 1;
    if (v_user_id = input_user_id or (select is_admin
                                      from user
                                      where user_id = input_user_id)=1)
    then
        if (select balance from Account where account_number = v_account_number) >= v_amount
            then
            if  v_is_loan_active = 1
                then
                select pay_date
                into v_date_to_pay
                from installment
                where loan_id = input_loan_id and
                      is_paid = 0
                order by pay_date
                limit 1;
                if v_date_to_pay is not null
                    then
                    update installment
                        set is_paid = 1,
                            pay_date = NOW()
                    where loan_id = input_loan_id and
                          pay_date = v_date_to_pay;
                    update Account
                        set balance = balance - v_amount
                    where account_number = v_account_number;
                    update loan
                        set installment_paid = installment_paid + 1
                    where loan_id = input_loan_id;
                    insert into Transaction(user_id,source_account_number,destination_account_number,amount,source_account_balance_after_transaction,destination_account_balance_after_transaction)
                    values (v_user_id,v_account_number,1,v_amount,(select balance
                                                                from Account
                                                                where account_number = v_account_number) - v_amount,(select balance
                                                                                                                   from Account
                                                                                                                   where account_number = 1) + v_amount);
                    if v_number_of_installment_left = 1
                        then
                        update Loan
                            set is_active = 0
                        where loan_id = input_loan_id;
                        update account
                            set active_loan_id = null
                        where account_number = v_account_number;
                    end if;
                    set x := true;
                else
                    set x := false;
                end if;
            else
                set x := false;
            end if;
        else
            set x := false;
        end if;
    else
        set x := false;
    end if;
    return x;
end;
