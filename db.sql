begin;

--------------TYPES----------------------

create type "media__type" as enum('image');

create table "media"(
"id" int primary key,
"path" varchar(50),
"name" varchar(20),
"mediatype" media__type
);

create type "gender__type" as enum (
'male',
'female',
'others'
);

create type "status__type" as enum (
'in-progress',
'completed'
);

create type "task__type" as enum (
'my_day',
'planned',
'assigned',
'custom'
);

create type product__type as enum(
'grocery',
'stationery',
'electronics',
'others'
);

create type theme__type as enum(
'color',
'image',
'none'
);

create type mode__type as enum(
'white',
'dark'
);

create type top_task__type as enum(
'in-progress',
'completed',
'priority'
);



-----------------------TABLES-------------------------------------------


create table "user"(
    "id" serial PRIMARY key,
    "name" varchar(30) not null,
    "email" VARCHAR(30) not null UNIQUE,
    "phone" VARCHAR(13) UNIQUE DEFAULT null,
    "password" varchar(30) not null,
	"dob" date not null,
	"gender" gender__type not null,
	"added_at" timestamp not null,
	"updated_at" timestamp DEFAULT null,
	"dp_id" int,
	"trash" boolean default false,
	foreign key("dp_id") references "media"("id")
);



create table "lists"(
    "id" serial PRIMARY key,
	"user_id" integer,
    "name" varchar(30) not null,
	"added_at" timestamp not null,
	"updated_at" timestamp default null,
	foreign key("user_id") references "user"("id")
);




create table "tasks"(
"id" serial primary key,
"user_id" integer,
"description" varchar(400),
"status" status__type,
"added_at" timestamp not null,
"updated_at" timestamp DEFAULT null,
"plan_start_date" timestamp default null,
"plan_end_date" timestamp DEFAULT null,
"actual_end_date" timestamp default null,
"duration" integer,
"task_type" task__type,
"notify" boolean default true,
"repeat" boolean default false,
"priority" boolean default false,
"list_id" integer,
foreign key("user_id") references "user"("id"),
foreign key("list_id") references "lists"("id")
);



create table "subtasks"(
"id" serial primary key,
"user_id" integer,
"task_id" integer,
"title" varchar(200),
"description" varchar(400),
"status" status__type,
"added_at" timestamp not null,
"updated_at" timestamp DEFAULT null,
"plan_start_date" timestamp default null,
"plan_end_date" timestamp DEFAULT null,
"actual_end_date" timestamp default null,
"duration" integer,
"task_type" task__type,
"notify" boolean default true,
"repeat" boolean default false,
"priority" boolean default false,
foreign key("user_id") references "user"("id"),
foreign key("task_id") references "tasks"("id")
);



create table "assigner_task"(
"assigner_user_id" integer,
"assignee_user_id" integer,
"task_id" integer,
"assigned_at" timestamp not null,
foreign key("assigner_user_id") references "user"("id"),
foreign key("assignee_user_id") references "user"("id"),
foreign key("task_id") references "tasks"("id"),
unique("assignee_user_id","task_id")
);





create table "basket"(
    "id" serial PRIMARY key,
	"user_id" integer,
    "product_name" varchar(30) not null,
	"s_type" status__type,
	"added_at" timestamp not null,
	"updated_at" timestamp default null,
	"p_type" product__type,
	"repeat" boolean default true,
	foreign key("user_id") references "user"("id")
);




create table "user_settings"(
	"user_id" integer,
	"theme_type" theme__type,
	"theme_color" varchar(10) default 'white',
	"background_image_id" integer default null,
    "confirm_deletion" boolean default false,
	"top_task_type" top_task__type default 'in-progress',
	"notify" boolean default true,
	"mode" mode__type default 'white',
	foreign key("user_id") references "user"("id"),
	foreign key("background_image_id") references "media"("id")
);

end;