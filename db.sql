begin;
--------------TYPES----------------------
create type "media__type" as enum ('image');
create type "gender__type" as enum ('male', 'female', 'other');
create type "status__type" as enum ('in-progress', 'completed');
create type "task__type" as enum ('my_day', 'planned', 'assigned', 'custom');
create type "product__type" as enum ('grocery', 'stationery', 'electronics', 'other');
create type "theme__type" as enum ('color', 'image', 'none');
create type "mode__type" as enum ('white', 'dark');
create type "top__task__type" as enum ('in-progress', 'completed', 'priority');
create type "event__type" as enum (
	'birthday',
	'marriage-anniversery',
	'death-anniversery',
	'holiday',
	'conference',
	'other'
);
create type "item__type" as enum (
	'milk',
	'water',
	'newspaper',
	'clothes',
	'other'
);
-----------------------TABLES-------------------------------------------
create table "media"(
	"id" int primary KEY,
	"name" varchar(20),
	"path" varchar(50),
	"mediatype" media__type
);
create table "users"(
	"id" serial PRIMARY KEY,
	"name" varchar not null,
	"email" VARCHAR not null UNIQUE,
	"phone" VARCHAR(13) UNIQUE DEFAULT NULL,
	"password" varchar not null,
	"dob" date not null,
	"gender" gender__type,
	"added_at" timestamp not null,
	"updated_at" timestamp DEFAULT null,
	"dp_id" int,
	"trash" boolean DEFAULT false,
	FOREIGN KEY("dp_id") references "media"("id") ON DELETE
	SET NULL
);
create table "lists"(
	"id" serial PRIMARY KEY,
	"user_id" integer,
	"name" varchar not null,
	"added_at" timestamp not null,
	"updated_at" timestamp DEFAULT null,
	FOREIGN KEY("user_id") references "users"("id") ON DELETE CASCADE
);
create table "tasks"(
	"id" serial primary KEY,
	"user_id" integer,
	"title" varchar,
	"description" varchar,
	"status" status__type,
	"added_at" timestamp not null,
	"updated_at" timestamp DEFAULT null,
	"plan_start_date" timestamp DEFAULT null,
	"plan_end_date" timestamp DEFAULT null,
	"actual_end_date" timestamp DEFAULT null,
	"duration" integer,
	"task_type" task__type,
	"notify" boolean DEFAULT true,
	"repeat" boolean DEFAULT false,
	"priority" boolean DEFAULT false,
	"list_id" integer,
	FOREIGN KEY("user_id") references "users"("id") ON DELETE CASCADE,
	FOREIGN KEY("list_id") references "lists"("id") ON DELETE CASCADE
);
create table "subtasks"(
	"id" serial primary KEY,
	"user_id" integer,
	"task_id" integer,
	"title" varchar,
	"description" varchar,
	"status" status__type,
	"added_at" timestamp not null,
	"updated_at" timestamp DEFAULT null,
	"plan_start_date" timestamp DEFAULT null,
	"plan_end_date" timestamp DEFAULT null,
	"actual_end_date" timestamp DEFAULT null,
	"duration" integer,
	"task_type" task__type,
	"notify" boolean DEFAULT true,
	"repeat" boolean DEFAULT false,
	"priority" boolean DEFAULT false,
	FOREIGN KEY("user_id") references "users"("id") ON DELETE CASCADE,
	FOREIGN KEY("task_id") references "tasks"("id") ON DELETE CASCADE
);
create table "assigned_tasks"(
	"assigner_user_id" integer,
	"assignee_user_id" integer,
	"task_id" integer,
	"assigned_at" timestamp not null,
	PRIMARY KEY("assignee_user_id", "task_id"),
	FOREIGN KEY("assigner_user_id") references "users"("id") ON DELETE
	SET NULL,
		FOREIGN KEY("assignee_user_id") references "users"("id") ON DELETE
	SET NULL,
		FOREIGN KEY("task_id") references "tasks"("id") ON DELETE CASCADE
);
create table "basket"(
	"id" serial PRIMARY KEY,
	"user_id" integer,
	"product_name" varchar not null,
	"status_type" status__type,
	"added_at" timestamp not null,
	"updated_at" timestamp DEFAULT null,
	"completed_at" timestamp DEFAULT null,
	"product_type" product__type,
	"repeat" boolean DEFAULT false,
	FOREIGN KEY("user_id") references "users"("id") ON DELETE CASCADE
);
create table "users_settings"(
	"user_id" integer,
	"theme_type" theme__type,
	"theme_color" varchar(10) DEFAULT 'white',
	"background_image_id" integer DEFAULT null,
	"confirm_deletion" boolean DEFAULT false,
	"top_task_type" top__task__type DEFAULT 'in-progress',
	"notify" boolean DEFAULT true,
	"mode" mode__type DEFAULT 'white',
	FOREIGN KEY("user_id") references "users"("id") ON DELETE CASCADE,
	FOREIGN KEY("background_image_id") references "media"("id") ON DELETE
	SET NULL
);
create table "events"(
	"id" serial primary KEY,
	"name" varchar,
	"user_id" integer,
	"added_at" timestamp not null,
	"updated_at" timestamp DEFAULT null,
	"event_type" event__type,
	"event_date" timestamp not null,
	"event_end_date" timestamp DEFAULT null,
	"notify" boolean DEFAULT true,
	"repeat" boolean DEFAULT false,
	FOREIGN KEY("user_id") references "users"("id") ON DELETE CASCADE
);
create table "bills"(
	"id" serial primary KEY,
	"user_id" integer,
	"added_at" timestamp not null,
	"updated_at" timestamp DEFAULT null,
	"rate" float not null,
	"quantity" float not null,
	"item_type" item__type,
	"paid" boolean DEFAULT false,
	"paid_at" timestamp DEFAULT null,
	FOREIGN KEY("user_id") references "users"("id") ON DELETE CASCADE
);
create table "monthly_bills"(
	"id" serial primary KEY,
	"user_id" integer,
	"cost" float not null,
	"item_type" item__type,
	FOREIGN KEY("user_id") references "users"("id") ON DELETE CASCADE
);
----- Indexes -----
CREATE INDEX ON "users" ("email");
CREATE INDEX ON "users" ("phone");
end;