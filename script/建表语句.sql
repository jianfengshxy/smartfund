CREATE TABLE IF NOT EXISTS `smartfund_user`(
`id` INT UNSIGNED AUTO_INCREMENT KEY COMMENT '用户编号',
`username` VARCHAR(20) NOT NULL UNIQUE COMMENT '用户名',
`password` CHAR(32) NOT NULL COMMENT '密码',
`tel` CHAR(11) NOT NULL UNIQUE COMMENT '电话',
`email` VARCHAR(50) NOT NULL UNIQUE COMMENT '邮箱',
`tt_password` CHAR(32) NOT NULL COMMENT '天天基金密码',
`tt_pay_password` CHAR(32) NOT NULL COMMENT '天天基金支付密码',
`group_name` CHAR(32) NOT NULL DEFAULT  '基础账户资产' COMMENT '基金组合',
`user_grade` VARCHAR(50) NOT NULL DEFAULT 'S1' COMMENT '用户等级',
`device` VARCHAR(20) NOT NULL DEFAULT  'SJE0217722000066'  COMMENT '绑定设备号',
`status` TINYINT(1) NOT NULL DEFAULT 0 COMMENT '0代表冻结，1代表有效',
`effective_date` DATE NOT NULL DEFAULT '2022-12-30' COMMENT '有效日期'
)ENGINE=INNODB DEFAULT CHARSET=UTF8

insert into `smartfund_user`( `username` , `password` , `tel` , `email` , `tt_password` , `tt_pay_password` )
values('jianfengshxy','sWX15706','13918199137','13918199137@139.com','sWX15706','sWX15706')

CREATE TABLE IF NOT EXISTS `fund_asset`(
 `id` INT UNSIGNED AUTO_INCREMENT KEY COMMENT '唯一id',
 `fund_code` VARCHAR(20) NOT NULL   COMMENT '基金代码',
 `date` DATE NOT NULL  COMMENT '日期',
 `tel` CHAR(32) NOT NULL COMMENT '持有人电话',
 `fund_unit` INT   NOT NULL DEFAULT  0  COMMENT  '全部份额',
 `fund_valid_unit` INT   NOT NULL DEFAULT 0  COMMENT  '可用份额',
 `income` INT   NOT NULL DEFAULT 0 COMMENT '持有收益',
 `income_rate` INT  NOT NULL DEFAULT 0 COMMENT '持有收益率'
)ENGINE=INNODB DEFAULT CHARSET=UTF8




CREATE TABLE IF NOT EXISTS `user_plan`(
 `id` INT UNSIGNED AUTO_INCREMENT KEY COMMENT '唯一id',
 `fund_code` VARCHAR(20) NOT NULL   COMMENT '基金代码',
 `tel` CHAR(32) NOT NULL COMMENT '持有人电话',
 `total` INT NOT NULL   DEFAULT 0  COMMENT '总的定投次数',
 `current_buy_number` INT NOT NULL   DEFAULT 0  COMMENT '当前期数',
 `start_date` DATE NOT NULL   COMMENT '当前定投开始的时间',
 `base_invest` INT   NOT NULL DEFAULT 1000  COMMENT  '定投基数',
 `percentage` INT   NOT NULL DEFAULT 5  COMMENT  '止盈百分比',
  `ratio` INT   NOT NULL DEFAULT 1 COMMENT '定投系数',
 `status` VARCHAR(20) NOT NULL  DEFAULT 'on'  COMMENT '定投状态'
)ENGINE=INNODB DEFAULT CHARSET=UTF8
insert into `user_plan`( `fund_code` , `tel` , `start_date` )
values('001618','13918199137','2021-01-07')
