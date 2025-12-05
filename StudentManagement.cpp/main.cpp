 // main.cpp
#include <bits/stdc++.h>
using namespace std;

const string STUD_FILE = "students.txt";
const string CRE_FILE  = "credentials.txt";

string currentUser;
string currentRole;

bool login() {
    string u, p, r;
    string inUser, inPass;

    cout << "USERNAME: ";
    if (!(cin >> inUser)) return false;
    cout << "PASSWORD: ";
    if (!(cin >> inPass)) return false;

    ifstream fin(CRE_FILE);
    if (!fin.is_open()) {
        cout << "Credential file missing!\n";
        return false;
    }

    while (fin >> u >> p >> r) {
        if (inUser == u && inPass == p) {
            currentUser = u;
            currentRole = r;
            fin.close();
            return true;
        }
    }

    fin.close();
    return false;
}

void addStudent() {
    int roll;
    string name;
    double mark;

    cout << "Roll: ";
    cin >> roll;
    cin.ignore(numeric_limits<streamsize>::max(), '\n');
    cout << "Name: ";
    getline(cin, name);
    cout << "Mark: ";
    cin >> mark;

    ofstream fo(STUD_FILE, ios::app);
    fo << roll << "|" << name << "|" << fixed << setprecision(2) << mark << '\n';
    fo.close();
    cout << "Student added!\n";
}

void displayStudents() {
    ifstream fi(STUD_FILE);
    if (!fi.is_open()) {
        cout << "No student file!\n";
        return;
    }
    cout << left << setw(8) << "Roll" << setw(30) << "Name" << setw(8) << "Mark" << "\n";
    cout << string(46, '-') << "\n";

    string line;
    while (getline(fi, line)) {
        if (line.empty()) continue;
        // format: roll|name|mark
        size_t p1 = line.find('|');
        size_t p2 = line.find('|', p1+1);
        if (p1==string::npos || p2==string::npos) continue;
        string roll = line.substr(0,p1);
        string name = line.substr(p1+1, p2-p1-1);
        string mark = line.substr(p2+1);
        cout << left << setw(8) << roll << setw(30) << name << setw(8) << mark << "\n";
    }
    fi.close();
}

void searchStudent() {
    cout << "Enter roll to search: ";
    int find; cin >> find;
    ifstream fi(STUD_FILE);
    if (!fi.is_open()) { cout << "No student file!\n"; return; }
    string line;
    while (getline(fi, line)) {
        if (line.empty()) continue;
        size_t p1 = line.find('|');
        size_t p2 = line.find('|', p1+1);
        if (p1==string::npos || p2==string::npos) continue;
        int roll = stoi(line.substr(0,p1));
        if (roll == find) {
            string name = line.substr(p1+1, p2-p1-1);
            string mark = line.substr(p2+1);
            cout << "Found: " << roll << " | " << name << " | " << mark << "\n";
            fi.close();
            return;
        }
    }
    fi.close();
    cout << "Student not found!\n";
}

void deleteStudent() {
    cout << "Enter roll to delete: ";
    int delRoll; cin >> delRoll;
    ifstream fi(STUD_FILE);
    if (!fi.is_open()) { cout << "No student file!\n"; return; }
    ofstream fo("temp.txt");
    string line;
    bool found = false;
    while (getline(fi, line)) {
        if (line.empty()) continue;
        size_t p1 = line.find('|');
        if (p1==string::npos) continue;
        int roll = stoi(line.substr(0,p1));
        if (roll != delRoll) fo << line << '\n';
        else found = true;
    }
    fi.close(); fo.close();
    if (found) {
        remove(STUD_FILE.c_str());
        rename("temp.txt", STUD_FILE.c_str());
        cout << "Student deleted!\n";
    } else {
        remove("temp.txt");
        cout << "Roll not found!\n";
    }
}

void updateStudent() {
    cout << "Enter roll to update: ";
    int updateRoll; cin >> updateRoll;
    ifstream fi(STUD_FILE);
    if (!fi.is_open()) { cout << "No student file!\n"; return; }
    ofstream fo("temp.txt");
    string line;
    bool found = false;
    while (getline(fi, line)) {
        if (line.empty()) continue;
        size_t p1 = line.find('|');
        size_t p2 = line.find('|', p1+1);
        if (p1==string::npos || p2==string::npos) continue;
        int roll = stoi(line.substr(0,p1));
        if (roll == updateRoll) {
            found = true;
            cin.ignore(numeric_limits<streamsize>::max(), '\n');
            cout << "New Name: ";
            string newName; getline(cin, newName);
            cout << "New Mark: ";
            double newMark; cin >> newMark;
            fo << roll << "|" << newName << "|" << fixed << setprecision(2) << newMark << '\n';
        } else {
            fo << line << '\n';
        }
    }
    fi.close(); fo.close();
    if (found) {
        remove(STUD_FILE.c_str());
        rename("temp.txt", STUD_FILE.c_str());
        cout << "Student updated!\n";
    } else {
        remove("temp.txt");
        cout << "Roll not found!\n";
    }
}

void adminMenu() {
    while (true) {
        cout << "\nADMIN MENU\n1.Add\n2.Display\n3.Search\n4.Update\n5.Delete\n6.Logout\nChoose: ";
        int c; if (!(cin >> c)) return;
        if (c==1) addStudent();
        else if (c==2) displayStudents();
        else if (c==3) searchStudent();
        else if (c==4) updateStudent();
        else if (c==5) deleteStudent();
        else return;
    }
}

void staffMenu() {
    while (true) {
        cout << "\nSTAFF MENU\n1.Add\n2.Display\n3.Search\n4.Update\n5.Logout\nChoose: ";
        int c; if (!(cin >> c)) return;
        if (c==1) addStudent();
        else if (c==2) displayStudents();
        else if (c==3) searchStudent();
        else if (c==4) updateStudent();
        else return;
    }
}

void guestMenu() {
    while (true) {
        cout << "\nGUEST MENU\n1.Display\n2.Search\n3.Logout\nChoose: ";
        int c; if (!(cin >> c)) return;
        if (c==1) displayStudents();
        else if (c==2) searchStudent();
        else return;
    }
}

int main() {
    cout << "=== Student Management System (C++) ===\n";
    if (!login()) {
        cout << "Invalid login!\n";
        return 0;
    }
    cout << "Logged in as: " << currentUser << " (role: " << currentRole << ")\n";
    if (currentRole == "admin") adminMenu();
    else if (currentRole == "staff") staffMenu();
    else guestMenu();
    cout << "Goodbye!\n";
    return 0;
}