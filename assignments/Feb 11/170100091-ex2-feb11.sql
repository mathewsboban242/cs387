ALTER TABLE takes ADD section_id integer;
ALTER TABLE section ADD id serial;
update takes 
set section_id=(select id from section where section.course_id = takes.course_id
and section.sec_id=takes.sec_id and section.semester = takes.semester and 
section.year = takes.year);
ALTER TABLE takes DROP CONSTRAINT takes_course_id_fkey;
ALTER TABLE teaches DROP CONSTRAINT teaches_course_id_fkey;
ALTER TABLE section DROP CONSTRAINT section_pkey;
ALTER TABLE section ADD PRIMARY KEY (ID);
ALTER TABLE takes ADD FOREIGN KEY (section_id) REFERENCES section(id);
ALTER TABLE takes DROP course_id;
ALTER TABLE takes DROP sec_id;
ALTER TABLE takes DROP semester;
ALTER TABLE takes DROP year;
ALTER TABLE section ADD UNIQUE (course_id,sec_id,year, semester);

ALTER TABLE teaches ADD section_id integer;
update teaches 
set section_id=(select id from section where section.course_id = teaches.course_id
and section.sec_id=teaches.sec_id and section.semester = teaches.semester and 
section.year = teaches.year);
ALTER TABLE teaches ADD FOREIGN KEY (section_id) REFERENCES section(id);
ALTER TABLE teaches DROP course_id;
ALTER TABLE teaches DROP sec_id;
ALTER TABLE teaches DROP semester;
ALTER TABLE teaches DROP year;

ALTER TABLE takes ADD student_id integer;
ALTER TABLE student RENAME COLUMN id TO student_id;
ALTER TABLE student ADD id serial;
ALTER TABLE student DROP CONSTRAINT student_pkey;
ALTER TABLE student ADD PRIMARY KEY (ID);
ALTER TABLE student ADD UNIQUE (student_id);
update takes set student_id= (select id from student where student.student_id = takes.id);
ALTER TABLE takes ADD FOREIGN KEY (student_id) REFERENCES student(student_id);
