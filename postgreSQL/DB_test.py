import DB_function


sql_str = """SELECT * FROM public.user_information
ORDER BY id ASC """

output = DB_function.DB_fetch(sql_str)
print(output)