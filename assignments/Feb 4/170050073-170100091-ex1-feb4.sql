create table addausers(loginname varchar(100) primary key, password varchar(100));
create table public.order (orderid serial primary key, loginname varchar(100) references addausers(loginname), datetime timestamp);
create table orderitem(orderid integer references public.order(orderid), item varchar(20), itemquantity numeric(5,0));