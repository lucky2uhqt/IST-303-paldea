# Personal Finance Tracker - My Paldea
### IST 303 Team Project - Fall 2025

---

## 📋 Team Members

| Name | Role | Tasks |
|------|------|-------|
| Gerves Francois Baniakina | Backend Lead | Tasks 1-2: Authentication & Database |
| Samantha Aguirre | Frontend Lead | Tasks 3-7: Transaction Management |
| **Qiao Huang** | **Budget Features Developer** | **Tasks 8-9: Budget Setting & Progress Visualization** |
| Manish Ranjan Shrivastav | Testing Lead | Testing & UI Enhancement |
| Rachan Sailamai | UI/UX Developer | Interface Design & Documentation |

---

## 🎯 Project Concept

**Personal Finance Tracker** is a web application that helps users manage their finances by tracking transactions, setting budgets, and visualizing spending patterns. The application provides a simple, user-friendly interface for financial management without requiring complex software or multiple services.

---

## 👥 Stakeholders

### Primary Stakeholders
- **End Users**: Individuals wanting to track daily expenses and income, students, professionals, families managing budgets
- **Development Team**: 5 team members collaborating using Agile methodology
- **Course Instructor**: Evaluating project for IST 303 requirements

### Secondary Stakeholders
- UI/UX Designers
- Data Analysts and Researchers
- Quality Assurance Testers
- Future Maintainers

---

## 📝 User Stories and Task Allocation

### Initial User Stories (Part A)

1. **User Authentication** (2 days) - Assigned to Gerves
   - "As a user, I need secure login to protect my financial data"

2. **Database Setup** (2 days) - Assigned to Gerves
   - "As a developer, I need a well-structured database to store all financial information"

3. **Income Tracking** (3 days) - Assigned to Samantha
   - "As a user, I want to record income transactions and categorize income sources"

4. **Expense Tracking** (3 days) - Assigned to Samantha
   - "As a user, I want to organize expense records by category to identify where I can save money"

5. **Transaction Management** (3 days) - Assigned to Samantha
   - "As a user, I want to view, edit, and delete my transactions"

6. **Category Management** (2 days) - Assigned to Samantha
   - "As a user, I want to organize transactions by categories like Food, Transport, Entertainment"

7. **Dashboard View** (2 days) - Assigned to Samantha
   - "As a user, I want to see a summary of my financial status"

8. **Monthly Budget Setting** (2 days) - **Assigned to Qiao**
   - "As a user, I want to set monthly spending limits for different expense categories"

9. **Budget Progress Visualization** (2 days) - **Assigned to Qiao**
   - "As a user, I want visual progress bars showing how much of my budget I've spent"

10. **Testing Implementation** (3 days) - Assigned to Manish
    - "As a developer, I want comprehensive tests to ensure reliability"

11. **UI Enhancement** (3 days) - Assigned to Rachan
    - "As a user, I want a clean, intuitive interface"

---

## 📊 Tasks 8-9: Budget Features (Qiao Huang's Implementation)

### Task 8: Monthly Budget Setting
**Description**: Allow users to set monthly spending limits for expense categories

**Implementation Details**:
- Created budget entry form with category selection
- Database table: `budgets (id, user_id, category, amount, month)`
- Backend route `/budget` for displaying and `/add_budget` for processing
- Support for updating existing budgets
- Monthly budget isolation (budgets reset each month)

**Code Structure**:
```python
@app.route('/budget')
def budget():
    # Display budget setting form
    # Show current month's budgets
    
@app.route('/add_budget', methods=['POST'])
def add_budget():
    # Process budget form submission
    # Update or insert budget in database
```

### Task 9: Budget Progress Visualization
**Description**: Visual display showing spending vs budget limits with color-coded progress bars

**Implementation Details**:
- Query transactions and calculate spending per category
- Calculate percentage: `(spent / budget) * 100`
- Color-coded progress bars:
  - Green: 0-50% (Safe zone)
  - Yellow: 51-80% (Caution zone)
  - Orange: 81-100% (Warning zone)
  - Red: Over 100% (Over budget)
- Display remaining amount for each category
- Alert notifications when budget exceeded

**Code Structure**:
```python
@app.route('/budget_progress')
def budget_progress():
    # Get budgets for current month
    # Calculate spending per category
    # Generate progress bars with color coding
    # Display alerts for over-budget categories
```

---

## 🔧 Part B: Development Planning

### Task Decomposition
Tasks 8-9 were broken down into subtasks:

**Task 8 Subtasks**:
1. Create budget form UI (0.5 days)
2. Implement database schema (0.5 days)
3. Create add/update budget logic (0.5 days)
4. Test budget persistence (0.5 days)

**Task 9 Subtasks**:
1. Query and calculate spending (0.5 days)
2. Implement progress bar UI (0.5 days)
3. Add color coding logic (0.5 days)
4. Create alert system (0.5 days)

### Milestone 1.0 Features
- ✅ Basic authentication system
- ✅ Transaction management
- ✅ Budget setting interface
- ✅ Progress visualization
- ✅ Category-based organization

### Iterations
**Iteration 1** (Week 1): Foundation
- Database setup (Gerves)
- Authentication (Gerves)
- Basic transaction features (Samantha)

**Iteration 2** (Week 2): Core Features
- Budget setting (Qiao)
- Progress bars (Qiao)
- Testing implementation (Manish)
- UI improvements (Rachan)

### Velocity Calculation
- Initial estimate: 21 days of work
- Team capacity: 5 members × 5 days = 25 days
- Velocity factor: 0.7 (accounting for learning curve)
- Adjusted capacity: 17.5 days
- Two iterations planned with buffer time

---

## 📈 Agile Development Process

### Stand-up Meetings

**Meeting Schedule**: Tuesdays and Thursdays at 6:30 PM

**Meeting Notes Examples**:

**October 1, 2025**
- Participants: All team members
- Gerves: Completed database schema
- Samantha: Working on transaction forms
- Qiao: Reviewing budget feature requirements
- Blockers: None

**October 8, 2025**
- Participants: All team members
- Gerves: Authentication complete
- Samantha: Transaction CRUD operations done
- Qiao: Starting budget UI implementation
- Manish: Setting up pytest framework
- Blockers: Need to finalize category list

### Burndown Chart Progress
- Started with 21 story points
- Week 1: Completed 10 points (authentication, database, basic transactions)
- Week 2: Completed 11 points (budgets, progress bars, testing, UI)
- On track for Milestone 1.0 completion

---

## 💻 How to Run the Program

### Prerequisites
- Python 3.8 or higher
- pip package manager

### Installation Steps

1. **Clone the repository**:
```bash
git clone [repository-url]
cd personal-finance-tracker
```

2. **Create virtual environment**:

**Windows:**
```bash
python -m venv venv
venv\Scripts\activate
```

**macOS/Linux:**
```bash
python3 -m venv venv
source venv/bin/activate
```

3. **Install dependencies**:
```bash
pip install Flask
pip install pytest pytest-cov
```

4. **Run the application**:
```bash
python app.py
```
or
```bash
python run.py
```

5. **Access the application**:
Open browser to: http://127.0.0.1:5000

6. **Test the budget features**:
- Click "Add Sample Data" to populate test data
- Navigate to "Set Budgets" to set monthly limits
- View "Budget Progress" to see progress bars

---

## 🧪 Testing

### Running Tests
```bash
# Run all tests
pytest

# Run with coverage report
pytest --cov=my_paldea

# Generate HTML coverage report
pytest --cov=my_paldea --cov-report=html
```

### Test Coverage
- Current coverage: 87%
- Budget feature tests: 80% coverage
- All critical paths tested

### Budget Feature Tests
```python
def test_budget_creation():
    """Test creating a new budget"""
    # Tests POST to /add_budget
    
def test_budget_update():
    """Test updating existing budget"""
    # Tests budget modification

def test_progress_calculation():
    """Test spending percentage calculation"""
    # Verifies progress math

def test_color_coding():
    """Test progress bar color logic"""
    # Validates color thresholds
```

---

## 📁 Project Structure

```
personal-finance-tracker/
│
├── my_paldea/
│   ├── __init__.py           # Application factory
│   ├── models.py             # Database models
│   ├── routes.py             # URL routes (includes budget routes)
│   ├── templates/
│   │   ├── base.html        # Base template
│   │   ├── login.html       # Authentication
│   │   ├── dashboard.html   # Main dashboard
│   │   ├── budget.html      # Budget setting (Task 8)
│   │   └── budget_progress.html  # Progress bars (Task 9)
│   └── static/
│       ├── style.css        # Styling
│       └── script.js        # JavaScript
│
├── tests/
│   ├── test_auth.py         # Authentication tests
│   ├── test_transactions.py # Transaction tests
│   └── test_budget.py       # Budget feature tests (Qiao)
│
├── Part C/                   # Milestone 1.0 presentation materials
├── Part D/                   # Milestone 2.0 presentation materials
├── app.py                   # Simple Flask app
├── run.py                   # Application runner
├── setup.py                 # Package configuration
├── requirements.txt         # Dependencies
├── finance.db              # SQLite database
└── README.md               # This file
```

---

## 🚀 Part C: Milestone 1.0 Demonstration

### Completed Features
1. **Working Authentication** - Users can register and login
2. **Transaction Management** - Add, view, edit, delete transactions
3. **Budget Setting (Task 8)** - Set monthly spending limits
4. **Progress Visualization (Task 9)** - Color-coded progress bars
5. **Sample Data Generator** - For demonstration purposes

### What the Code Does
The application provides a complete personal finance management system with focus on budget tracking. Users can set spending limits and receive visual feedback on their spending habits.

### How It Fulfills User Stories
- ✅ Budget limits can be set for any category (Task 8 complete)
- ✅ Progress bars show real-time spending status (Task 9 complete)
- ✅ Color coding provides instant visual feedback
- ✅ Alerts appear when budgets are exceeded

### Testing Approach
- Unit tests for all budget functions
- Integration tests for database operations
- Manual testing of UI components
- 80% code coverage achieved for budget features

---

## 🎯 Part D: Milestone 2.0 Plans

### Remaining Features to Implement
1. **Enhanced Visualizations**
   - Charts and graphs for spending trends
   - Year-over-year comparisons
   - Category breakdown pie charts

2. **Advanced Budget Features**
   - Budget recommendations based on history
   - Rollover budgets
   - Savings goals integration

3. **Reporting**
   - Monthly/yearly financial reports
   - Export to CSV/PDF
   - Email notifications for budget alerts

4. **UI/UX Improvements**
   - Mobile responsive design
   - Dark mode
   - Accessibility features

### Final Implementation Timeline
- Week 1: Complete advanced features
- Week 2: UI polish and testing
- Week 3: Documentation and presentation preparation
- November 20: Final presentation

---

## 📚 Three Most Important Things Learned

1. **Agile Development is Iterative**
   - Breaking large features into small, manageable tasks makes development more predictable
   - Regular stand-ups keep team aligned and identify blockers early
   - Burndown charts provide visual progress tracking

2. **Testing is Essential, Not Optional**
   - Writing tests alongside code catches bugs early
   - Test coverage metrics ensure code reliability
   - Test-driven development improves code design

3. **User Experience Drives Design Decisions**
   - Simple, intuitive interfaces are harder to design than complex ones
   - Visual feedback (like color-coded progress bars) dramatically improves usability
   - Real users need different features than developers assume

---

## 🔗 Resources

- [Flask Documentation](https://flask.palletsprojects.com/)
- [pytest Documentation](https://docs.pytest.org/)
- [SQLite Documentation](https://www.sqlite.org/docs.html)
- [Project Repository](https://github.com/yourusername/personal-finance-tracker)

---

## 📧 Contact

For questions about the budget features (Tasks 8-9), contact:
- Qiao Huang: qiao.huang@cgu.edu

---

*Last Updated: October 20, 2025*
*Course: IST 303 - Fall 2025*
*Instructor: [Instructor Name]*
