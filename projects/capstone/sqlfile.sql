--
-- PostgreSQL database dump
--

-- Dumped from database version 13.1
-- Dumped by pg_dump version 13.1

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
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
-- Name: actor; Type: TABLE; Schema: public; Owner: senor
--

CREATE TABLE public.actor (
    id integer NOT NULL,
    name character varying(50) NOT NULL,
    age integer NOT NULL,
    gender character varying(10) NOT NULL
);


ALTER TABLE public.actor OWNER TO senor;

--
-- Name: actor_id_seq; Type: SEQUENCE; Schema: public; Owner: senor
--

CREATE SEQUENCE public.actor_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.actor_id_seq OWNER TO senor;

--
-- Name: actor_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: senor
--

ALTER SEQUENCE public.actor_id_seq OWNED BY public.actor.id;


--
-- Name: casting; Type: TABLE; Schema: public; Owner: senor
--

CREATE TABLE public.casting (
    actor_id integer,
    movie_id integer
);


ALTER TABLE public.casting OWNER TO senor;

--
-- Name: movie; Type: TABLE; Schema: public; Owner: senor
--

CREATE TABLE public.movie (
    id integer NOT NULL,
    title character varying(250) NOT NULL,
    genres character varying(120) NOT NULL,
    year integer
);


ALTER TABLE public.movie OWNER TO senor;

--
-- Name: movie_id_seq; Type: SEQUENCE; Schema: public; Owner: senor
--

CREATE SEQUENCE public.movie_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.movie_id_seq OWNER TO senor;

--
-- Name: movie_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: senor
--

ALTER SEQUENCE public.movie_id_seq OWNED BY public.movie.id;


--
-- Name: actor id; Type: DEFAULT; Schema: public; Owner: senor
--

ALTER TABLE ONLY public.actor ALTER COLUMN id SET DEFAULT nextval('public.actor_id_seq'::regclass);


--
-- Name: movie id; Type: DEFAULT; Schema: public; Owner: senor
--

ALTER TABLE ONLY public.movie ALTER COLUMN id SET DEFAULT nextval('public.movie_id_seq'::regclass);


--
-- Data for Name: actor; Type: TABLE DATA; Schema: public; Owner: senor
--

COPY public.actor (id, name, age, gender) FROM stdin;
\.


--
-- Data for Name: casting; Type: TABLE DATA; Schema: public; Owner: senor
--

COPY public.casting (actor_id, movie_id) FROM stdin;
\.


--
-- Data for Name: movie; Type: TABLE DATA; Schema: public; Owner: senor
--

COPY public.movie (id, title, genres, year) FROM stdin;
\.


--
-- Name: actor_id_seq; Type: SEQUENCE SET; Schema: public; Owner: senor
--

SELECT pg_catalog.setval('public.actor_id_seq', 2, true);


--
-- Name: movie_id_seq; Type: SEQUENCE SET; Schema: public; Owner: senor
--

SELECT pg_catalog.setval('public.movie_id_seq', 1, true);


--
-- Name: actor actor_pkey; Type: CONSTRAINT; Schema: public; Owner: senor
--

ALTER TABLE ONLY public.actor
    ADD CONSTRAINT actor_pkey PRIMARY KEY (id);


--
-- Name: movie movie_pkey; Type: CONSTRAINT; Schema: public; Owner: senor
--

ALTER TABLE ONLY public.movie
    ADD CONSTRAINT movie_pkey PRIMARY KEY (id);


--
-- Name: casting casting_actor_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: senor
--

ALTER TABLE ONLY public.casting
    ADD CONSTRAINT casting_actor_id_fkey FOREIGN KEY (actor_id) REFERENCES public.actor(id);


--
-- Name: casting casting_movie_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: senor
--

ALTER TABLE ONLY public.casting
    ADD CONSTRAINT casting_movie_id_fkey FOREIGN KEY (movie_id) REFERENCES public.movie(id);


--
-- PostgreSQL database dump complete
--

