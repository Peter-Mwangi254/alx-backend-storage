-- Creates a stored procedure AddBonus
-- that adds a new correction for a student.

DELIMITER //

CREATE PROCEDURE AddBonus(
	IN `user_id` INTEGER,
	IN `project_name` VARCHAR(255),
	IN `score` INTEGER
)
BEGIN
    INSERT INTO projects (name)
    SELECT project_name
    -- WHERE NOT EXISTS (SELECT * FROM projects WHERE name=project_name LIMIT 1);
    WHERE project_name NOT IN (SELECT name FROM projects);

    INSERT INTO corrections (user_id, project_id, score)
    VALUES(user_id, (SELECT id from projects WHERE name=project_name), score);
END;
//

DELIMITER;
