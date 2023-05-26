# NOTES

## using raw sql for migrating data with alembic.
There was an issue executing `flask db upgrade`, as expected, because it was trying to add a unique contraint, when there was already data conflicting.
So, I decided to try and address is, as it would need to be addressed, in a real siutation, assuming whoever would be doing this would need to 
have the unique contraint applied. 
Intead of direclty deleiting, or truncating rows, I decieded to use the `op` from alembic, as the scripts do. 

First I found what sql I wanted, then added it to the upgrade command, before applying the uqniqe contraint.
see migrations\versions\20230508_5b24e2438219_.py


### sql to delte existing duplicates, before adding a contraint using the migration.  
    with dups as (select t1.* from teachers_students t1 inner join (select * from teachers_students ) as t2 on t1.student_id = t2.student_id and t1.teacher_id = t2.teacher_id and coalesce(t1.class_name,'') = coalesce(t2.class_name,'')),
    to_keep as (select max(id) as id from dups group by teacher_id, student_id, class_name having count(*) > 0),
    to_delete as (select distinct id from dups where id not in (select id from to_keep))
    delete from teachers_students where id in (select * from to_delete);


    with dups as (select t1.* from teachers_students t1 inner join (select * from teachers_students ) as t2 on t1.student_id = t2.student_id and t1.teacher_id = t2.teacher_id and coalesce(t1.class_name,'') = coalesce(t2.class_name,'')), to_keep as (select max(id) as id from dups group by teacher_id, student_id, class_name ) select * from to_keep;

### op command

    query = "my sql query"
    op.execute(query).

this was gleaned from this post 
https://alembic.sqlalchemy.org/en/latest/ops.html#alembic.operations.Operations.execute


## deleting a linked table
   table.delete().where(table.c.id==7)

   for multiple, i had to add multiple where, like this...

        delete = (
            teachers_students.delete()
            .where(teachers_students.c.student_id == student.id)
            .where(teachers_students.c.teacher_id == teacher.id)
            .where(teachers_students.c.class_name == str(classname))
        )
        result = db.session.execute(delete)
        db.session.commit()


## deleting a teacher.
I ran into this error, when tring the basic delete on a teacher.

    sqlalchemy.orm.exc.StaleDataError: DELETE statement on table 'teachers_students' expected to delete 1 row(s); Only 2 were matched.

I realized. I thought it might have something to do with having teacher_id be a primary key, so
I tried something else.
I created a teach called "No Instructor", wich had the ID 3. 
Instead of deleting it outright, I update to the 3 id.
Then do db.commit, and them delete the teach from the route id in the url

This made me realize it's a function that could be similar for switching a teacher, if needed.

That seems like a good put, but since there is the added complexity of class_name being part of the key,
I'd need to specify if it's for all classes, or a particular class
TODO:


