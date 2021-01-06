# Global variables
table_list = ["Customers", "Orders"]
attr_list_customer = ["Customers.Name", "Customers.Age"]
attr_list_orders = ["Orders.CustomerName", "Orders.Product", "Orders.Price"]
op_list = ['<>', '<=', '>=', "=", '>', '<']
string_value = ["Customers.Name", "Orders.CustomerName", "Orders.Product"]
int_value = ["Customers.Age", "Orders.Price"]
apostrophe_list = ["'", "\""]
# apostrophe_list = ["'", "\"", "’"]
AND_EXPRESSION = " AND "
OR_EXPRESSION = " OR "
OPEN_BRACKET = "("
CLOSE_BRACKET = ")"
COMMA = ","


########## Function checks the "SELECT" query  ##########
def is_attribute_list(user_query: str, table_list: list):
    user_query = user_query.strip()
    list_words = user_query.split()

    if len(list_words) == 0:
        return False

    if len(list_words) == 1:
        if list_words[0] == '*':
            return True

    if len(list_words) == 2:
        if list_words[0] == "DISTINCT" and list_words[1] == "*":
            return True

    if list_words[0] == "DISTINCT":
        user_query = user_query[8:]
    return is_attribute_list_rec(user_query, table_list)


# Rec Function checks if input is attribute list
def is_attribute_list_rec(user_query: str, table_list: list):
    if is_valid_attribute(user_query, table_list):
        return True

    comma_index = user_query.find(COMMA)
    if comma_index == -1:
        return False

    attr = user_query[0:comma_index]
    attrList = user_query[comma_index + 1:]
    return is_valid_attribute(attr, table_list) and is_attribute_list_rec(attrList, table_list)


# Function gets input and check if is a valid attribute from Customers and Orders list
def is_valid_attribute(input_string: str, table_list: list):
    input_string = input_string.strip()

    res = False;
    if "Customers" in table_list:
        if input_string in attr_list_customer:
            res = True
    if "Orders" in table_list:
        if input_string in attr_list_orders:
            res = True
    return res


########## Function checks the "FROM" query ##########
def is_table_list(user_query: str):
    if is_valid_table(user_query):
        return True

    comma_index = user_query.find(COMMA)
    if comma_index == -1:
        return False

    table_name = user_query[0:comma_index]
    table_list = user_query[comma_index + 1:]
    return is_valid_table(table_name) and is_table_list(table_list)


# Aux Funcion that check if the table is valid
def is_valid_table(user_query: str):
    return user_query.strip() in table_list


########## Function checks the "WHERE" query ##########
def is_condition(user_query: str, table_list):
    user_query = user_query.strip()
    query_len = len(user_query)

    if query_len > 2 and user_query[0] == OPEN_BRACKET and user_query[query_len - 1] == CLOSE_BRACKET:
        if is_condition(user_query[1:query_len - 1], table_list):
            return True

    # get list of start indexes of and expressions - AND|OR
    listOfIndexes = find_all(user_query, AND_EXPRESSION) + find_all(user_query, OR_EXPRESSION)

    for ex_start_index in listOfIndexes:
        ex_end_index = get_end_index_expression(user_query[ex_start_index:], ex_start_index)
        left_condition = user_query[0:ex_start_index]
        right_condition = user_query[ex_end_index:]
        if is_condition(left_condition, table_list) and is_condition(right_condition, table_list):
            return True

    return is_simple_condition(user_query, table_list)


# Function checks if is simple condition
def is_simple_condition(condition: str, table_list: list):
    condition = condition.strip()

    if find_rel_op(condition) == -1:
        return False

    op_start_index = find_rel_op(condition)
    op_end_index = get_end_index_operator(condition[op_start_index:], op_start_index)  # "Yair" = Coustmer.Name
    constant_1 = condition[0:op_start_index].strip()
    constant_2 = condition[op_end_index:].strip()
    return is_constant(constant_1, table_list) and is_constant(constant_2, table_list) and is_values_type_match(
        constant_1, constant_2)


# Function checks if two attrs are from the same type
def is_values_type_match(constant_1: str, constant_2: str):
    res = False

    if is_int(constant_1) and (is_int(constant_2) or constant_2 in int_value):
        res = True
    if is_string(constant_1) and (is_string(constant_2) or constant_2 in string_value):
        res = True
    if constant_1 in string_value and (constant_2 in string_value or is_string(constant_2)):
        res = True
    if constant_1 in int_value and (constant_2 in int_value or is_int(constant_2)):
        res = True
    return res


# Function checks if const is valid
def is_constant(constant_str: str, table_list):
    constant_str = constant_str.strip()
    return is_int(constant_str) or is_string(constant_str) or is_valid_attribute(constant_str, table_list)


########## AUXILARY FUNCTIONS ##########
# Function checks if value is int type
def is_int(value):
    try:
        int(value)
        return True
    except ValueError:
        return False


# Function checks if value is string type
def is_string(value):
    if len(value) > 1:
        return value[0] in apostrophe_list and value[len(value) - 1] == value[0];
    return False


# Function return the index of the first operator in string
def find_rel_op(condition: str):
    res = -1
    for i in op_list:
        res = condition.find(i)
        if res != -1:
            break
    return res


# Function returns indexes of all the occurrences of a substring in a string
def find_all(a_string, sub):
    result = []
    k = 0
    while k < len(a_string):
        k = a_string.find(sub, k)
        if k == -1:
            return result
        else:
            result.append(k)
            k += 1
    return result


# Function return end index of the expression (AND/OR)
def get_end_index_expression(cond_query, start_index):
    if cond_query.startswith(AND_EXPRESSION):
        return start_index + len(AND_EXPRESSION)
    if cond_query.startswith(OR_EXPRESSION):
        return start_index + len(OR_EXPRESSION)
    return -1


# Function return end index of the operator (AND/OR)
def get_end_index_operator(cond_query, start_index):
    for op in ['<>', '<=', '>=']:
        if cond_query.startswith(op):
            return start_index + 2
    for op in ['=', '>', '<']:
        if cond_query.startswith(op):
            return start_index + 1
    return -1


# Function that gets the wrong part of query and prints error msg
def print_error_message(msg: str):
    print("Invalid Query")
    print("Parsing <" + msg.strip() + "> failed")


################## MAIN ##################
def main():
    user_input = input("Enter Your SQL Query: ").strip()

    idx_select = user_input.find("SELECT")
    idx_from = user_input.find("FROM")
    idx_where = user_input.find("WHERE")

    if not user_input[len(user_input) - 1] == ";":
        print("missing ; in end of query")
        return

    userselect = user_input[idx_select + len("SELECT"):idx_from]
    userfrom = user_input[idx_from + len("FROM"):idx_where]
    userwhere = user_input[idx_where + len("WHERE"):len(user_input) - 1]

    # FROM
    if not is_table_list(userfrom):
        print_error_message("table_list")
        return

    # SELECT
    table_list = userfrom.replace(',', ' ').split()
    if not is_attribute_list(userselect, table_list):
        print_error_message("attribute_list")
        return

    # WHERE
    if not is_condition(userwhere, table_list):
        print_error_message("condition")
        return

    print("Valid Query")


main()
