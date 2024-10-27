--
-- PostgreSQL database dump
--

-- Dumped from database version 17.0 (Postgres.app)
-- Dumped by pg_dump version 17.0 (Postgres.app)

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET transaction_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SELECT pg_catalog.set_config('search_path', '', false);
SET check_function_bodies = false;
SET xmloption = content;
SET client_min_messages = warning;
SET row_security = off;

SET default_tablespace = '';

SET default_table_access_method = heap;

--
-- Name: attachments; Type: TABLE; Schema: public; Owner: denis
--

CREATE TABLE public.attachments (
    id integer NOT NULL,
    event_id integer NOT NULL,
    filename character varying(100) NOT NULL,
    filepath character varying(200) NOT NULL,
    upload_time timestamp without time zone NOT NULL
);


ALTER TABLE public.attachments OWNER TO denis;

--
-- Name: attachments_id_seq; Type: SEQUENCE; Schema: public; Owner: denis
--

CREATE SEQUENCE public.attachments_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.attachments_id_seq OWNER TO denis;

--
-- Name: attachments_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: denis
--

ALTER SEQUENCE public.attachments_id_seq OWNED BY public.attachments.id;


--
-- Name: events; Type: TABLE; Schema: public; Owner: denis
--

CREATE TABLE public.events (
    id integer NOT NULL,
    user_id integer NOT NULL,
    title character varying(100) NOT NULL,
    start_time timestamp without time zone NOT NULL,
    end_time timestamp without time zone NOT NULL,
    description character varying(500),
    date date NOT NULL,
    attachment character varying(100)
);


ALTER TABLE public.events OWNER TO denis;

--
-- Name: events_id_seq; Type: SEQUENCE; Schema: public; Owner: denis
--

CREATE SEQUENCE public.events_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.events_id_seq OWNER TO denis;

--
-- Name: events_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: denis
--

ALTER SEQUENCE public.events_id_seq OWNED BY public.events.id;


--
-- Name: users; Type: TABLE; Schema: public; Owner: denis
--

CREATE TABLE public.users (
    id integer NOT NULL,
    username character varying(64) NOT NULL,
    email character varying(120) NOT NULL,
    password_hash character varying(256) NOT NULL,
    salt character varying(32) NOT NULL
);


ALTER TABLE public.users OWNER TO denis;

--
-- Name: users_id_seq; Type: SEQUENCE; Schema: public; Owner: denis
--

CREATE SEQUENCE public.users_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.users_id_seq OWNER TO denis;

--
-- Name: users_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: denis
--

ALTER SEQUENCE public.users_id_seq OWNED BY public.users.id;


--
-- Name: attachments id; Type: DEFAULT; Schema: public; Owner: denis
--

ALTER TABLE ONLY public.attachments ALTER COLUMN id SET DEFAULT nextval('public.attachments_id_seq'::regclass);


--
-- Name: events id; Type: DEFAULT; Schema: public; Owner: denis
--

ALTER TABLE ONLY public.events ALTER COLUMN id SET DEFAULT nextval('public.events_id_seq'::regclass);


--
-- Name: users id; Type: DEFAULT; Schema: public; Owner: denis
--

ALTER TABLE ONLY public.users ALTER COLUMN id SET DEFAULT nextval('public.users_id_seq'::regclass);


--
-- Data for Name: attachments; Type: TABLE DATA; Schema: public; Owner: denis
--

COPY public.attachments (id, event_id, filename, filepath, upload_time) FROM stdin;
\.


--
-- Data for Name: events; Type: TABLE DATA; Schema: public; Owner: denis
--

COPY public.events (id, user_id, title, start_time, end_time, description, date, attachment) FROM stdin;
25	1	event	2024-10-27 12:30:00	2024-10-27 13:30:00	event	2024-10-27	221-329__6.docx
\.


--
-- Data for Name: users; Type: TABLE DATA; Schema: public; Owner: denis
--

COPY public.users (id, username, email, password_hash, salt) FROM stdin;
1	den	denrus2003@mail.ru	scrypt:32768:8:1$5f1wJfEfdmCcSari$f41fdbf3dc118d7c2f887494f6f4236efbd7c4a8056e96020060993504766ff98358f4bf702c75eb1117ed5ad28f0874031d20005071a4761492e8b3d2ba97ab	531f9ce73eb8dfeaa04c5684a23c26e8
2	1	denverrus2003@gmail.com	scrypt:32768:8:1$WZwHQczmfxA5XgQO$4b6b3f651f96a14e2cff2f10703b1042b5201b8e1bfab6d56c8e92355126721968278dc0c527caad86c0800e31258e5acdc55a91310ff7f851312d0656f02929	2fc9b4286a07c77d1a3abe9b2f8979eb
\.


--
-- Name: attachments_id_seq; Type: SEQUENCE SET; Schema: public; Owner: denis
--

SELECT pg_catalog.setval('public.attachments_id_seq', 1, false);


--
-- Name: events_id_seq; Type: SEQUENCE SET; Schema: public; Owner: denis
--

SELECT pg_catalog.setval('public.events_id_seq', 25, true);


--
-- Name: users_id_seq; Type: SEQUENCE SET; Schema: public; Owner: denis
--

SELECT pg_catalog.setval('public.users_id_seq', 2, true);


--
-- Name: attachments attachments_pkey; Type: CONSTRAINT; Schema: public; Owner: denis
--

ALTER TABLE ONLY public.attachments
    ADD CONSTRAINT attachments_pkey PRIMARY KEY (id);


--
-- Name: events events_pkey; Type: CONSTRAINT; Schema: public; Owner: denis
--

ALTER TABLE ONLY public.events
    ADD CONSTRAINT events_pkey PRIMARY KEY (id);


--
-- Name: users users_email_key; Type: CONSTRAINT; Schema: public; Owner: denis
--

ALTER TABLE ONLY public.users
    ADD CONSTRAINT users_email_key UNIQUE (email);


--
-- Name: users users_pkey; Type: CONSTRAINT; Schema: public; Owner: denis
--

ALTER TABLE ONLY public.users
    ADD CONSTRAINT users_pkey PRIMARY KEY (id);


--
-- Name: users users_username_key; Type: CONSTRAINT; Schema: public; Owner: denis
--

ALTER TABLE ONLY public.users
    ADD CONSTRAINT users_username_key UNIQUE (username);


--
-- Name: attachments attachments_event_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: denis
--

ALTER TABLE ONLY public.attachments
    ADD CONSTRAINT attachments_event_id_fkey FOREIGN KEY (event_id) REFERENCES public.events(id);


--
-- Name: events events_user_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: denis
--

ALTER TABLE ONLY public.events
    ADD CONSTRAINT events_user_id_fkey FOREIGN KEY (user_id) REFERENCES public.users(id);


--
-- PostgreSQL database dump complete
--

