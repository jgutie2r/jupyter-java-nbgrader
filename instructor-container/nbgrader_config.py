c = get_config()
c.CourseDirectory.course_id = "Tareas"
c.CourseDirectory.root="/home/jovyan/Tareas"

# This is the folder where the asigments will be stored to deliver via jupyterhub
c.Exchange.root = "/srv/nbgrader/exchange"

c.ClearSolutions.begin_solution_delimeter = "BSOL"
c.ClearSolutions.end_solution_delimeter = "ESOL"

# Short names for BEGIN SOLUTION and for BEGIN HIDDEN TESTS
c.ClearHiddenTests.begin_test_delimeter = "BTEST"
c.ClearHiddenTests.end_test_delimeter = "ETEST"
