CREATE TABLE IF NOT EXISTS public.migration_controller ( modification integer NOT NULL );

DO
$do$
DECLARE
	modific integer;
  tmp_modific integer;
  last_modific integer;
  patient001 uuid;
  patient002 uuid;
  patient003 uuid;
  patient004 uuid;
  physician001 uuid;
  physician002 uuid;
BEGIN
  raise notice 'Starting DB Migration';

  IF NOT EXISTS (SELECT FROM migration_controller) THEN
    INSERT INTO migration_controller VALUES (1);
  END IF;

  LOCK TABLE migration_controller IN EXCLUSIVE MODE;

  -- GET modification number
  SELECT modification into modific FROM migration_controller;
  last_modific := modific;
  LOOP
    raise notice 'Running step %', modific;

    tmp_modific := modific;

    -- Migrations
    IF modific=1 THEN
      CREATE TABLE IF NOT EXISTS public.patient (
        id uuid NOT NULL DEFAULT  gen_random_uuid() ,
        "name" varchar(255) NOT NULL,
        CONSTRAINT patient_pk PRIMARY KEY (id)
      );
      CREATE INDEX patient_name_idx ON public.patient ("name");

      modific := modific + 1;
    END IF;

    IF modific=2 THEN
      CREATE TABLE IF NOT EXISTS public.physician (
        id uuid NOT NULL DEFAULT  gen_random_uuid() ,
        "name" varchar(255) NOT NULL,
        CONSTRAINT physician_pk PRIMARY KEY (id)
      );
      CREATE INDEX physician_name_idx ON public.physician ("name");

      modific := modific + 1;
    END IF;    

    IF modific=3 THEN
      CREATE TABLE public.appointment (
        id uuid NOT NULL DEFAULT gen_random_uuid(),
        start_date timestamp(0) NOT NULL,
        end_date timestamp(0) NULL,
        patient_id uuid NOT NULL,
        physician_id uuid NOT NULL,
        price float8 NULL,
        CONSTRAINT appointment_pk PRIMARY KEY (id)
      );
      CREATE INDEX appointment_patient_id_idx ON public.appointment USING btree (patient_id);
      CREATE INDEX appointment_physician_id_idx ON public.appointment USING btree (physician_id);
      CREATE INDEX appointment_start_date_idx ON public.appointment USING btree (start_date);

      -- public.appointment foreign keys
      ALTER TABLE public.appointment ADD CONSTRAINT appointment_patient_fk FOREIGN KEY (patient_id) REFERENCES public.patient(id);
      ALTER TABLE public.appointment ADD CONSTRAINT appointment_physician_fk FOREIGN KEY (physician_id) REFERENCES public.physician(id);

      modific := modific + 1;
    END IF;
    
    IF modific=4 THEN
      CREATE TABLE public.charge (
        id uuid NOT NULL DEFAULT gen_random_uuid(),
        appointment_id uuid NOT NULL,
        amount float8 NOT NULL,
        CONSTRAINT charge_pk PRIMARY KEY (id)
      );
      CREATE INDEX charge_appointment_id_idx ON public.charge USING btree (appointment_id);

      -- public.charge foreign keys
      ALTER TABLE public.charge ADD CONSTRAINT charge_fk FOREIGN KEY (appointment_id) REFERENCES public.appointment(id);      -- modific := modific + 1;

      modific := modific + 1;
    END IF;

    IF modific=5 THEN
        insert into patient (name) values ('Patient 01') RETURNING id INTO patient001;
        insert into patient (name) values ('Patient 02') RETURNING id INTO patient002;
        insert into patient (name) values ('Patient 03') RETURNING id INTO patient003;
        insert into patient (name) values ('Patient 04') RETURNING id INTO patient004;
        insert into physician (name) values ('physician 01') RETURNING id INTO physician001;
        insert into physician (name) values ('physician 02') RETURNING id INTO physician002;
        insert into appointment (start_date, patient_id, physician_id) VALUES (NOW(), patient001, physician001);
        insert into appointment (start_date, patient_id, physician_id) VALUES (NOW(), patient002, physician001);
        insert into appointment (start_date, patient_id, physician_id) VALUES (NOW(), patient003, physician002);
        insert into appointment (start_date, patient_id, physician_id) VALUES (NOW(), patient004, physician002);
      modific := modific + 1;
    END IF;

    IF modific=6 THEN
      -- Put here the next script and uncommend the line below
      -- modific := modific + 1;
    END IF;

    EXIT WHEN modific = tmp_modific;
  END LOOP;
  IF not last_modific = modific THEN
    update migration_controller set modification = modific;
  END IF;
  raise notice 'DB Migration finished';
END
$do$
