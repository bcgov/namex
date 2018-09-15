
  -- Drops

  DROP TABLE IF EXISTS public.synonym_audit CASCADE;

  DROP TABLE IF EXISTS public.synonym CASCADE;

  DROP SEQUENCE IF EXISTS public.synonym_audit_id_seq;

  DROP SEQUENCE IF EXISTS public.synonym_id_seq;

  DROP TYPE IF EXISTS public.audit_action;

  -- Creates

  CREATE TYPE public.audit_action AS ENUM ('CREATE', 'DELETE', 'UPDATE');

  CREATE SEQUENCE public.synonym_audit_id_seq;

  CREATE TABLE public.synonym_audit
  (
      id integer NOT NULL DEFAULT nextval('synonym_audit_id_seq'::regclass),
      synonym_id integer NOT NULL,
      username character varying(100) COLLATE pg_catalog."default" DEFAULT ''::character varying,
      action audit_action,
      timestamp timestamp DEFAULT clock_timestamp(),
      category character varying(100) COLLATE pg_catalog."default" DEFAULT ''::character varying,
      synonyms_text character varying(1000) COLLATE pg_catalog."default",
      comment character varying(1000) COLLATE pg_catalog."default" DEFAULT ''::character varying,
      enabled boolean,
      CONSTRAINT synonym_audit_pkey PRIMARY KEY (id),
      CONSTRAINT synonym_audit_username_not_null CHECK (username IS NOT NULL) NOT VALID,
      CONSTRAINT synonym_audit_action_not_null CHECK (action IS NOT NULL) NOT VALID
  )
  WITH (
      OIDS = FALSE
  )
  TABLESPACE pg_default;

  CREATE SEQUENCE public.synonym_id_seq;

  CREATE TABLE public.synonym
  (
      id integer NOT NULL DEFAULT nextval('synonym_id_seq'::regclass),
      category character varying(100) COLLATE pg_catalog."default" DEFAULT ''::character varying,
      synonyms_text character varying(1000) COLLATE pg_catalog."default",
      comment character varying(1000) COLLATE pg_catalog."default" DEFAULT ''::character varying,
      enabled boolean DEFAULT true,
      CONSTRAINT synonym_pkey PRIMARY KEY (id),
      CONSTRAINT synonyms_text_unique UNIQUE (synonyms_text),
      CONSTRAINT synonyms_text_not_null CHECK (synonyms_text IS NOT NULL) NOT VALID
  )
  WITH (
      OIDS = FALSE
  )
  TABLESPACE pg_default;
