-- 从成交表插入主键
insert into times_daily (account,vari,date)
select distinct account,vari,tradedate from chengjiao;

-- 从平仓表补充剩余的主键
insert ignore into times_daily (account,vari,date)
select distinct account,vari,tradedate from pingcang;

-- 插入开仓次数
update times_daily set open_times=(select count(*) from chengjiao
where chengjiao.account=times_daily.account and chengjiao.vari=times_daily.vari and tradedate=date and eo_flag='0');

-- 插入做多次数
update times_daily set long_times=(select count(*) from chengjiao
where chengjiao.account=times_daily.account and chengjiao.vari=times_daily.vari and tradedate=date and bs_flag='0' and eo_flag='0');

-- 插入做空次数
update times_daily set short_times=(select count(*) from chengjiao
where chengjiao.account=times_daily.account and chengjiao.vari=times_daily.vari and tradedate=date and bs_flag='1' and eo_flag='0');

-- 插入平仓次数
update times_daily set drop_times=(select count(distinct done_no)
from pingcang where pingcang.account=times_daily.account and pingcang.vari=times_daily.vari and tradedate=date);

-- 插入平今次数
update times_daily set today_drop_times=(select count(distinct done_no)
from pingcang where pingcang.account=times_daily.account and pingcang.vari=times_daily.vari and tradedate=date and tradedate=open_date);

-- 插入总次数
update times_daily set times=open_times+drop_times;

-- 插入all品种
-- insert into times_daily (account,code,date,times,open_times,drop_times,long_times,short_times,today_drop_times)
-- select account,'all',date,sum(times),sum(open_times),sum(drop_times),sum(long_times),sum(short_times),sum(today_drop_times)
-- from times_daily group by account,date;
