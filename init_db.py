#!/usr/bin/env python3
"""
Database Initialization Script
Personal Finance Tracker - My Paldea
Developer: Qiao Huang (Tasks 8-9)
Course: IST 303 Fall 2025
"""

import sqlite3
import os
from datetime import datetime, timedelta
import random

def create_database():
    """Create and initialize the database with all required tables"""
    
    # Remove existing database for fresh start (optional)
    if os.path.exists('finance.db'):
        print("⚠️  Existing database found. Backing up...")
        os.rename('finance.db', f'finance_backup_{datetime.now().strftime("%Y%m%d_%H%M%S")}.db')
    
    # Create new database connection
    conn = sqlite3.connect('finance.db')
    c = conn.cursor()
    
    print("📊 Creating database tables...")
    
    # Create users table
    c.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            email TEXT UNIQUE,
            password_hash TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    print("✅ Users table created")
    
    # Create transactions table
    c.execute('''
        CREATE TABLE IF NOT EXISTS transactions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            amount DECIMAL(10, 2) NOT NULL,
            category TEXT NOT NULL,
            description TEXT,
            date DATE NOT NULL,
            type TEXT NOT NULL CHECK (type IN ('income', 'expense')),
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users (id)
        )
    ''')
    print("✅ Transactions table created")
    
    # Create budgets table (Task 8)
    c.execute('''
        CREATE TABLE IF NOT EXISTS budgets (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            category TEXT NOT NULL,
            amount DECIMAL(10, 2) NOT NULL,
            month TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users (id),
            UNIQUE(user_id, category, month)
        )
    ''')
    print("✅ Budgets table created (Task 8)")
    
    # Create categories table
    c.execute('''
        CREATE TABLE IF NOT EXISTS categories (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT UNIQUE NOT NULL,
            icon TEXT,
            color TEXT,
            type TEXT CHECK (type IN ('income', 'expense', 'both'))
        )
    ''')
    print("✅ Categories table created")
    
    # Create indexes for better performance
    c.execute('CREATE INDEX IF NOT EXISTS idx_transactions_user ON transactions (user_id)')
    c.execute('CREATE INDEX IF NOT EXISTS idx_transactions_date ON transactions (date)')
    c.execute('CREATE INDEX IF NOT EXISTS idx_budgets_user_month ON budgets (user_id, month)')
    print("✅ Database indexes created")
    
    conn.commit()
    conn.close()
    print("✅ Database structure complete!")

def add_default_categories():
    """Add default expense and income categories"""
    conn = sqlite3.connect('finance.db')
    c = conn.cursor()
    
    print("\n📁 Adding default categories...")
    
    categories = [
        # Expense categories
        ('Food', '🍔', '#FF6B6B', 'expense'),
        ('Transportation', '🚗', '#4ECDC4', 'expense'),
        ('Entertainment', '🎬', '#45B7D1', 'expense'),
        ('Shopping', '🛍️', '#F7B801', 'expense'),
        ('Utilities', '💡', '#95E77E', 'expense'),
        ('Healthcare', '🏥', '#FF6B9D', 'expense'),
        ('Education', '📚', '#C44569', 'expense'),
        ('Housing', '🏠', '#7B68EE', 'expense'),
        ('Insurance', '🛡️', '#00B894', 'expense'),
        ('Other', '📌', '#636E72', 'expense'),
        
        # Income categories
        ('Salary', '💰', '#00D2D3', 'income'),
        ('Freelance', '💻', '#54A0FF', 'income'),
        ('Investment', '📈', '#48DBFB', 'income'),
        ('Business', '🏢', '#0ABDE3', 'income'),
        ('Other Income', '💵', '#006BA6', 'income')
    ]
    
    for name, icon, color, cat_type in categories:
        try:
            c.execute('''
                INSERT OR IGNORE INTO categories (name, icon, color, type)
                VALUES (?, ?, ?, ?)
            ''', (name, icon, color, cat_type))
        except sqlite3.IntegrityError:
            pass  # Category already exists
    
    conn.commit()
    conn.close()
    print("✅ Default categories added")

def add_demo_data():
    """Add demonstration data for testing"""
    conn = sqlite3.connect('finance.db')
    c = conn.cursor()
    
    print("\n🧪 Adding demo data...")
    
    # Add demo user
    from werkzeug.security import generate_password_hash
    
    demo_password = generate_password_hash('demo123')
    try:
        c.execute('''
            INSERT INTO users (username, email, password_hash)
            VALUES (?, ?, ?)
        ''', ('demo', 'demo@example.com', demo_password))
        print("✅ Demo user created (username: demo, password: demo123)")
    except sqlite3.IntegrityError:
        print("ℹ️  Demo user already exists")
    
    # Get demo user ID
    user_id = c.execute('SELECT id FROM users WHERE username = ?', ('demo',)).fetchone()[0]
    
    current_month = datetime.now().strftime('%Y-%m')
    
    # Add demo budgets for current month (Task 8)
    demo_budgets = [
        ('Food', 600.00),
        ('Transportation', 250.00),
        ('Entertainment', 200.00),
        ('Shopping', 300.00),
        ('Utilities', 350.00),
        ('Healthcare', 150.00)
    ]
    
    print("📊 Adding demo budgets...")
    for category, amount in demo_budgets:
        c.execute('''
            INSERT OR REPLACE INTO budgets (user_id, category, amount, month)
            VALUES (?, ?, ?, ?)
        ''', (user_id, category, amount, current_month))
    
    # Add demo transactions for progress visualization (Task 9)
    print("💰 Adding demo transactions...")
    
    # Generate transactions for current month
    today = datetime.now()
    transactions = [
        # Food expenses (will be at ~70% of budget)
        ('Food', 125.50, today - timedelta(days=15), 'expense', 'Grocery shopping'),
        ('Food', 45.00, today - timedelta(days=12), 'expense', 'Restaurant lunch'),
        ('Food', 89.99, today - timedelta(days=10), 'expense', 'Weekly groceries'),
        ('Food', 32.50, today - timedelta(days=7), 'expense', 'Coffee and snacks'),
        ('Food', 127.00, today - timedelta(days=3), 'expense', 'Grocery shopping'),
        
        # Transportation (will be at ~40% of budget)
        ('Transportation', 50.00, today - timedelta(days=14), 'expense', 'Gas'),
        ('Transportation', 25.00, today - timedelta(days=8), 'expense', 'Uber rides'),
        ('Transportation', 30.00, today - timedelta(days=2), 'expense', 'Gas'),
        
        # Entertainment (will be at ~90% of budget - warning level)
        ('Entertainment', 65.00, today - timedelta(days=13), 'expense', 'Movie tickets'),
        ('Entertainment', 45.00, today - timedelta(days=9), 'expense', 'Concert'),
        ('Entertainment', 70.00, today - timedelta(days=4), 'expense', 'Theme park'),
        
        # Shopping (will be over budget - red alert!)
        ('Shopping', 150.00, today - timedelta(days=11), 'expense', 'Clothing'),
        ('Shopping', 89.99, today - timedelta(days=6), 'expense', 'Electronics'),
        ('Shopping', 120.00, today - timedelta(days=1), 'expense', 'Home decor'),
        
        # Utilities (will be at ~30% of budget - green)
        ('Utilities', 105.00, today - timedelta(days=5), 'expense', 'Electric bill'),
        
        # Income transactions
        ('Salary', 3000.00, today - timedelta(days=15), 'income', 'Monthly salary'),
        ('Freelance', 500.00, today - timedelta(days=8), 'income', 'Web design project')
    ]
    
    for category, amount, date, trans_type, description in transactions:
        c.execute('''
            INSERT INTO transactions (user_id, category, amount, date, type, description)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (user_id, category, amount, date.strftime('%Y-%m-%d'), trans_type, description))
    
    conn.commit()
    conn.close()
    print("✅ Demo data added successfully!")

def display_summary():
    """Display database summary"""
    conn = sqlite3.connect('finance.db')
    c = conn.cursor()
    
    print("\n📊 Database Summary:")
    print("=" * 50)
    
    # Count records in each table
    tables = ['users', 'transactions', 'budgets', 'categories']
    for table in tables:
        count = c.execute(f'SELECT COUNT(*) FROM {table}').fetchone()[0]
        print(f"  {table.capitalize()}: {count} records")
    
    # Show budget progress for demo user
    current_month = datetime.now().strftime('%Y-%m')
    budgets = c.execute('''
        SELECT b.category, b.amount,
               COALESCE(SUM(t.amount), 0) as spent
        FROM budgets b
        LEFT JOIN transactions t ON 
            t.user_id = b.user_id AND 
            t.category = b.category AND 
            strftime('%Y-%m', t.date) = b.month AND
            t.type = 'expense'
        WHERE b.user_id = 1 AND b.month = ?
        GROUP BY b.category, b.amount
    ''', (current_month,)).fetchall()
    
    if budgets:
        print("\n📈 Demo User Budget Progress (Current Month):")
        print("-" * 50)
        for category, budget, spent in budgets:
            percentage = (spent / budget * 100) if budget > 0 else 0
            remaining = budget - spent
            
            # Determine status emoji
            if percentage <= 50:
                status = "✅"
            elif percentage <= 80:
                status = "⚠️"
            elif percentage <= 100:
                status = "🔶"
            else:
                status = "🔴"
            
            print(f"  {status} {category}:")
            print(f"     Budget: ${budget:.2f} | Spent: ${spent:.2f}")
            print(f"     Progress: {percentage:.0f}% | Remaining: ${remaining:.2f}")
    
    conn.close()
    print("=" * 50)

def main():
    """Main initialization function"""
    print("\n" + "="*50)
    print("💰 PERSONAL FINANCE TRACKER - DATABASE SETUP")
    print("="*50)
    print("Developer: Qiao Huang")
    print("Tasks: 8 (Budget Setting) & 9 (Progress Visualization)")
    print("="*50 + "\n")
    
    try:
        # Create database structure
        create_database()
        
        # Add default categories
        add_default_categories()
        
        # Ask user if they want demo data
        response = input("\n❓ Add demo data for testing? (y/n): ").lower()
        if response == 'y':
            add_demo_data()
        
        # Display summary
        display_summary()
        
        print("\n✅ Database initialization complete!")
        print("📌 You can now run the application with: python app.py")
        
    except Exception as e:
        print(f"\n❌ Error during initialization: {str(e)}")
        print("Please check your Python installation and try again.")

if __name__ == '__main__':
    main()
