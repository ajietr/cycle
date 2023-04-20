import json
import numpy as np


# 从本地文件加载JSON数据
def load_json_data(file_path):
    with open(file_path, "r", encoding="utf-8") as file:
        return json.load(file)


# 增加科室数量
def expand_departments(student, departments):
    expanded_departments = []
    for department_id in student["department_ids"]:
        department = next((dept for dept in departments if dept["id"] == department_id), None)
        if department:
            duration = int(department["rotation_duration"])
            expanded_departments.extend([department_id] * duration)
    return expanded_departments


def calculate_monthly_capacity(departments, total_students):
    total_durations = {dept["id"]: int(dept["rotation_duration"]) for dept in departments}
    total_duration = sum(total_durations.values())
    monthly_capacity = {dept_id: int(duration * total_students / total_duration) for dept_id, duration in
                        total_durations.items()}
    return monthly_capacity


def main():
    students_file = "students.json"
    departments_file = "departments.json"

    raw_students_data = load_json_data(students_file)
    students_data = raw_students_data["students"]  # 获取students列表
    departments_data = load_json_data(departments_file)

    expanded_students_departments = []

    for student in students_data:  # 直接遍历students列表
        expanded_departments = expand_departments(student, departments_data)
        expanded_students_departments.append(expanded_departments)

    total_students = len(students_data)
    monthly_capacity = calculate_monthly_capacity(departments_data, total_students)

    print("Monthly capacity for each department:")
    for dept_id, capacity in monthly_capacity.items():
        print(f"Department {dept_id}: {capacity} students")

    rotation_matrix = np.array(expanded_students_departments)

    print("\nRotation matrix:")
    print(rotation_matrix)


if __name__ == "__main__":
    main()
