
CREATE TABLE IF NOT EXISTS public.employees
(
    emp_id varchar(6) NOT NULL,
    login varchar(255) NOT NULL,
    name varchar(255) NOT NULL,
    salary numeric(12,2) NOT NULL,
    CONSTRAINT employees_pkey PRIMARY KEY (emp_id),
    CONSTRAINT employees_login_key UNIQUE (login)
)