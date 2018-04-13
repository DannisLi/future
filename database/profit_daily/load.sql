-- 确定profit_daily的主键
-- 从平仓表和持仓表提取主键，因为收益可分为平仓产生和持仓产生
insert into profit_daily (account,vari,date)
select distinct account,vari,tradedate from pingcang;

insert ignore into profit_daily (account,vari,date)
select distinct account,vari,tradedate from chicang;

-- 计算drop_profit
update profit_daily set drop_profit=(select (case when sum(drop_profit_d) is NULL then 0 else sum(drop_profit_d) end) from pingcang
where pingcang.account=profit_daily.account and pingcang.vari=vari and tradedate=date);

-- 计算hold_profit
update profit_daily set hold_profit=(select (case when sum(hold_profit_d) is NULL then 0 else sum(hold_profit_d) end) from chicang
where chicang.account=profit_daily.account and chicang.vari=profit_daily.vari and tradedate=date);

-- 计算pos_profit（分平仓、持仓）
update profit_daily set pos_profit=(select (case when sum(drop_profit_d) is NULL then 0 else sum(drop_profit_d) end) from pingcang
where pingcang.account=profit_daily.account and pingcang.vari=profit_daily.vari and tradedate=date and drop_profit_d>0);

update profit_daily set pos_profit=pos_profit+(select (case when sum(hold_profit_d) is NULL then 0 else sum(hold_profit_d) end) from chicang
where chicang.account=profit_daily.account and chicang.vari=profit_daily.vari and tradedate=date and hold_profit_d>0);

-- 计算neg_profit（分平仓、持仓）
update profit_daily set neg_profit=(select (case when sum(drop_profit_d) is NULL then 0 else sum(drop_profit_d) end) from pingcang
where pingcang.account=profit_daily.account and pingcang.vari=profit_daily.vari and tradedate=date and drop_profit_d<0);

update profit_daily set neg_profit=neg_profit+(select (case when sum(hold_profit_d) is NULL then 0 else sum(hold_profit_d) end) from chicang
where chicang.account=profit_daily.account and chicang.vari=profit_daily.vari and tradedate=date and hold_profit_d<0);

-- 计算profit
update profit_daily set profit=drop_profit+hold_profit;

-- 计算"all"
insert into profit_daily (account,vari,date,profit,drop_profit,hold_profit,pos_profit,neg_profit)
select account,"all",date,sum(profit),sum(drop_profit),sum(hold_profit),sum(pos_profit),sum(neg_profit)
from profit_daily group by account,date;
