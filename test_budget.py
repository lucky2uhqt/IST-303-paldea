# test_budget.py - Tests for Budget Features (Tasks 8-9)
# Developer: Qiao Huang
# Course: IST 303 Fall 2025

import pytest
import sqlite3
import os
from datetime import datetime
from budget_routes import init_budget_tables, get_budget_summary

# Import your Flask app (adjust import based on your structure)
# from app import app, init_db
# OR
# from my_paldea import create_app

# For standalone testing, create a simple test app
from flask import Flask
from budget_routes import budget_bp

def create_test_app():
    """Create Flask app for testing"""
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'test-secret-key'
    app.config['TESTING'] = True
    app.register_blueprint(budget_bp)
    return app

@pytest.fixture
def app():
    """Create and configure test app"""
    app = create_test_app()
    
    # Initialize test database
    init_budget_tables()
    
    # Add test data
    conn = sqlite3.connect('finance.db')
    c = conn.cursor()
    
    # Create test user
    c.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY,
            username TEXT UNIQUE,
            password_hash TEXT
        )
    ''')
    
    c.execute('''
        INSERT OR IGNORE INTO users (id, username, password_hash) 
        VALUES (1, 'testuser', 'hashed_password')
    ''')
    
    # Create transactions table for testing
    c.execute('''
        CREATE TABLE IF NOT EXISTS transactions (
            id INTEGER PRIMARY KEY,
            user_id INTEGER,
            amount DECIMAL,
            category TEXT,
            date DATE,
            type TEXT
        )
    ''')
    
    conn.commit()
    conn.close()
    
    yield app
    
    # Cleanup after tests
    if os.path.exists('finance.db'):
        os.remove('finance.db')

@pytest.fixture
def client(app):
    """Create test client"""
    return app.test_client()

# TASK 8 TESTS: Monthly Budget Setting

def test_budget_table_creation():
    """Test that budget tables are created correctly"""
    init_budget_tables()
    
    conn = sqlite3.connect('finance.db')
    c = conn.cursor()
    
    # Check if budgets table exists
    table_check = c.execute('''
        SELECT name FROM sqlite_master 
        WHERE type='table' AND name='budgets'
    ''').fetchone()
    
    conn.close()
    
    assert table_check is not None
    assert table_check[0] == 'budgets'

def test_add_new_budget():
    """Test adding a new budget"""
    conn = sqlite3.connect('finance.db')
    c = conn.cursor()
    
    # Initialize tables
    init_budget_tables()
    
    # Add a budget
    c.execute('''
        INSERT INTO budgets (user_id, category, amount, month)
        VALUES (1, 'Food', 500.00, '2025-10')
    ''')
    conn.commit()
    
    # Verify budget was added
    budget = c.execute('''
        SELECT * FROM budgets 
        WHERE user_id = 1 AND category = 'Food'
    ''').fetchone()
    
    conn.close()
    
    assert budget is not None
    assert budget[2] == 'Food'  # category
    assert budget[3] == 500.00  # amount

def test_update_existing_budget():
    """Test updating an existing budget"""
    conn = sqlite3.connect('finance.db')
    c = conn.cursor()
    
    init_budget_tables()
    
    # Add initial budget
    c.execute('''
        INSERT INTO budgets (user_id, category, amount, month)
        VALUES (1, 'Food', 500.00, '2025-10')
    ''')
    conn.commit()
    
    # Update the budget
    c.execute('''
        UPDATE budgets 
        SET amount = 600.00 
        WHERE user_id = 1 AND category = 'Food' AND month = '2025-10'
    ''')
    conn.commit()
    
    # Verify update
    budget = c.execute('''
        SELECT amount FROM budgets 
        WHERE user_id = 1 AND category = 'Food'
    ''').fetchone()
    
    conn.close()
    
    assert budget[0] == 600.00

def test_delete_budget():
    """Test deleting a budget"""
    conn = sqlite3.connect('finance.db')
    c = conn.cursor()
    
    init_budget_tables()
    
    # Add budget
    c.execute('''
        INSERT INTO budgets (user_id, category, amount, month)
        VALUES (1, 'Food', 500.00, '2025-10')
    ''')
    conn.commit()
    
    # Delete budget
    c.execute('''
        DELETE FROM budgets 
        WHERE user_id = 1 AND category = 'Food'
    ''')
    conn.commit()
    
    # Verify deletion
    budget = c.execute('''
        SELECT * FROM budgets 
        WHERE user_id = 1 AND category = 'Food'
    ''').fetchone()
    
    conn.close()
    
    assert budget is None

def test_budget_unique_constraint():
    """Test that duplicate budgets for same category/month are prevented"""
    conn = sqlite3.connect('finance.db')
    c = conn.cursor()
    
    init_budget_tables()
    
    # Add first budget
    c.execute('''
        INSERT INTO budgets (user_id, category, amount, month)
        VALUES (1, 'Food', 500.00, '2025-10')
    ''')
    conn.commit()
    
    # Try to add duplicate (should fail or update)
    try:
        c.execute('''
            INSERT INTO budgets (user_id, category, amount, month)
            VALUES (1, 'Food', 600.00, '2025-10')
        ''')
        conn.commit()
        duplicate_allowed = True
    except sqlite3.IntegrityError:
        duplicate_allowed = False
    
    conn.close()
    
    assert not duplicate_allowed  # Should not allow duplicates

# TASK 9 TESTS: Budget Progress Visualization

def test_calculate_spending_percentage():
    """Test calculation of spending percentage against budget"""
    budget_amount = 500.00
    spent_amount = 250.00
    
    percentage = (spent_amount / budget_amount) * 100
    
    assert percentage == 50.0

def test_progress_color_coding():
    """Test that correct colors are assigned based on percentage"""
    test_cases = [
        (25, 'success'),     # 25% = Green
        (50, 'success'),     # 50% = Green
        (70, 'warning'),     # 70% = Yellow
        (85, 'danger-orange'), # 85% = Orange
        (110, 'danger')      # 110% = Red (over budget)
    ]
    
    for percentage, expected_color in test_cases:
        if percentage <= 50:
            color = 'success'
        elif percentage <= 80:
            color = 'warning'
        elif percentage <= 100:
            color = 'danger-orange'
        else:
            color = 'danger'
        
        assert color == expected_color, f"Failed for {percentage}%"

def test_calculate_remaining_budget():
    """Test calculation of remaining budget amount"""
    budget = 500.00
    spent = 350.00
    
    remaining = budget - spent
    
    assert remaining == 150.00

def test_over_budget_detection():
    """Test detection of over-budget scenarios"""
    test_cases = [
        (500, 400, False),  # Under budget
        (500, 500, False),  # Exactly at budget
        (500, 600, True)    # Over budget
    ]
    
    for budget, spent, expected_over in test_cases:
        is_over = spent > budget
        assert is_over == expected_over

def test_budget_progress_with_transactions():
    """Test budget progress calculation with actual transactions"""
    conn = sqlite3.connect('finance.db')
    c = conn.cursor()
    
    init_budget_tables()
    
    # Add budget
    c.execute('''
        INSERT INTO budgets (user_id, category, amount, month)
        VALUES (1, 'Food', 500.00, '2025-10')
    ''')
    
    # Add transactions
    transactions = [
        (1, 'Food', 120.00, '2025-10-01', 'expense'),
        (1, 'Food', 80.00, '2025-10-05', 'expense'),
        (1, 'Food', 50.00, '2025-10-10', 'expense')
    ]
    
    for user_id, category, amount, date, type_ in transactions:
        c.execute('''
            INSERT INTO transactions (user_id, category, amount, date, type)
            VALUES (?, ?, ?, ?, ?)
        ''', (user_id, category, amount, date, type_))
    
    conn.commit()
    
    # Calculate spending
    spent = c.execute('''
        SELECT COALESCE(SUM(amount), 0) 
        FROM transactions 
        WHERE user_id = 1 AND category = 'Food' 
        AND strftime('%Y-%m', date) = '2025-10'
        AND type = 'expense'
    ''').fetchone()[0]
    
    conn.close()
    
    assert spent == 250.00
    percentage = (spent / 500.00) * 100
    assert percentage == 50.0

def test_multiple_category_budgets():
    """Test handling multiple budget categories"""
    conn = sqlite3.connect('finance.db')
    c = conn.cursor()
    
    init_budget_tables()
    
    # Add multiple budgets
    budgets = [
        ('Food', 500),
        ('Transportation', 200),
        ('Entertainment', 150)
    ]
    
    for category, amount in budgets:
        c.execute('''
            INSERT INTO budgets (user_id, category, amount, month)
            VALUES (1, ?, ?, '2025-10')
        ''', (category, amount))
    
    conn.commit()
    
    # Get all budgets
    all_budgets = c.execute('''
        SELECT category, amount FROM budgets 
        WHERE user_id = 1 AND month = '2025-10'
        ORDER BY category
    ''').fetchall()
    
    conn.close()
    
    assert len(all_budgets) == 3
    assert all_budgets[0][0] == 'Entertainment'
    assert all_budgets[1][0] == 'Food'
    assert all_budgets[2][0] == 'Transportation'

def test_monthly_budget_isolation():
    """Test that budgets are isolated by month"""
    conn = sqlite3.connect('finance.db')
    c = conn.cursor()
    
    init_budget_tables()
    
    # Add budgets for different months
    c.execute('''
        INSERT INTO budgets (user_id, category, amount, month)
        VALUES (1, 'Food', 500.00, '2025-09')
    ''')
    
    c.execute('''
        INSERT INTO budgets (user_id, category, amount, month)
        VALUES (1, 'Food', 600.00, '2025-10')
    ''')
    
    conn.commit()
    
    # Get October budget
    oct_budget = c.execute('''
        SELECT amount FROM budgets 
        WHERE user_id = 1 AND category = 'Food' AND month = '2025-10'
    ''').fetchone()
    
    # Get September budget
    sep_budget = c.execute('''
        SELECT amount FROM budgets 
        WHERE user_id = 1 AND category = 'Food' AND month = '2025-09'
    ''').fetchone()
    
    conn.close()
    
    assert oct_budget[0] == 600.00
    assert sep_budget[0] == 500.00

def test_budget_summary():
    """Test budget summary calculation"""
    conn = sqlite3.connect('finance.db')
    c = conn.cursor()
    
    init_budget_tables()
    
    # Add test budgets
    budgets = [
        ('Food', 500),
        ('Transportation', 200),
        ('Entertainment', 300)
    ]
    
    for category, amount in budgets:
        c.execute('''
            INSERT INTO budgets (user_id, category, amount, month)
            VALUES (1, ?, ?, '2025-10')
        ''', (category, amount))
    
    conn.commit()
    conn.close()
    
    # Get summary
    summary = get_budget_summary(1, '2025-10')
    
    assert summary['total_categories'] == 3
    assert summary['total_budget'] == 1000.00
    assert summary['min_budget'] == 200.00
    assert summary['max_budget'] == 500.00

# Integration tests
def test_budget_page_loads(client):
    """Test that budget page loads successfully"""
    response = client.get('/budget/')
    assert response.status_code in [200, 302]  # 302 if login required

def test_progress_page_loads(client):
    """Test that progress page loads successfully"""
    response = client.get('/budget/progress')
    assert response.status_code in [200, 302]  # 302 if login required

# Run tests
if __name__ == '__main__':
    pytest.main([__file__, '-v'])
