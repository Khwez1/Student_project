-- Q1
SELECT s.name, COUNT(e.course_id) FROM students s
LEFT JOIN enrollments e ON s.student_id = e.student_id
GROUP BY s.name
-- Q2
SELECT c.name, AVG(e.mark) FROM courses c
LEFT JOIN enrollments e ON c.course_id = e.course_id
Group by c.name
-- Q3
SELECT s.name, AVG(e.mark) AS marks FROM students s
LEFT JOIN enrollments e ON s.student_id = e.student_id
HAVING marks > 70
GROUP BY s.name
-- Q4
SELECT s.city, COUNT(e.enrol_id) FROM students s
LEFT JOIN enrollments e ON s.student_id = e.student_id
GROUP BY s.city
-- Q5
SELECT c.name, AVG(e.mark), COUNT(e.student_id) AS students_number FROM courses c
LEFT JOIN enrollments e ON c.course_id = e.course_id
HAVING students_number
GROUP BY e.course_id
-- MEMORANDUM
-- Q4
SELECT s.city, COUNT(e.enrol_id) AS total_enrolments
FROM students s
JOIN enrolments e ON s.student_id = e.student_id
GROUP BY s.city
HAVING COUNT(e.enrol_id) > 1;
-- Q3
SELECT s.name, AVG(e.mark) AS avg_mark
FROM students s
JOIN enrolments e ON s.student_id = e.student_id
GROUP BY s.name
HAVING AVG(e.mark) > 70;
-- Q5
SELECT c.course_name, MAX(e.mark) AS highest_mark, COUNT(e.student_id) AS students_number
FROM courses c
JOIN enrolments e ON c.course_id = e.course_id
GROUP BY c.course_id, c.course_name
HAVING COUNT(e.student_id) >= 2;