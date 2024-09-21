select
	`class`,
    `numGuns`
from
    `Classes`
where
	numGuns = (select max(`numGuns`) from `Classes`);
