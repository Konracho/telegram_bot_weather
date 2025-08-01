--
-- PostgreSQL database dump
--

-- Dumped from database version 17.5
-- Dumped by pg_dump version 17.5

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
-- Name: BD_cityes; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public."BD_cityes" (
    id integer,
    city text,
    city_rus text
);


ALTER TABLE public."BD_cityes" OWNER TO postgres;

--
-- Name: cities; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.cities (
    id integer NOT NULL,
    city character varying(255),
    city_rus character varying(255)
);


ALTER TABLE public.cities OWNER TO postgres;

--
-- Data for Name: BD_cityes; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public."BD_cityes" (id, city, city_rus) FROM stdin;
4079	sankt-peterburg	╤Б╨░╨╜╨║╤В-╨┐╨╡╤В╨╡╤А╨▒╤Г╤А╨│
4327	tver	╤В╨▓╨╡╤А╤М
4517	yekaterinburg	╨╡╨║╨░╤В╨╡╤А╨╕╨╜╨▒╤Г╤А╨│
4877	vladivostok	╨▓╨╗╨░╨┤╨╕╨▓╨╛╤Б╤В╨╛╨║
4368	moscow	╨╝╨╛╤Б╨║╨▓╨░
11959	dubna	╨┤╤Г╨▒╨╜╨░
\.


--
-- Data for Name: cities; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.cities (id, city, city_rus) FROM stdin;
4079	sankt-peterburg	╤Б╨░╨╜╨║╤В-╨┐╨╡╤В╨╡╤А╨▒╤Г╤А╨│
4327	tver	╤В╨▓╨╡╤А╤М
4517	yekaterinburg	╨╡╨║╨░╤В╨╡╤А╨╕╨╜╨▒╤Г╤А╨│
4877	vladivostok	╨▓╨╗╨░╨┤╨╕╨▓╨╛╤Б╤В╨╛╨║
4368	moscow	╨╝╨╛╤Б╨║╨▓╨░
11959	dubna	╨┤╤Г╨▒╨╜╨░
\.


--
-- Name: cities cityes_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.cities
    ADD CONSTRAINT cityes_pkey PRIMARY KEY (id);


--
-- PostgreSQL database dump complete
--

