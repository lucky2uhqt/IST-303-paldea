# budget_routes.py - Budget Feature Implementation
# Developer: Qiao Huang
# Tasks: 8 (Monthly Budget Setting) & 9 (Progress Bar Visualization)
# Course: IST 303 Fall 2025

from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify
from flask_login import login_required, current_user
import sqlite3
from datetime import datetime
import calendar

# Create blueprint for budget routes
budget_bp = Blueprint('budget', __name__, url_prefix='/budget')

def get_db_connection():
    """Create database connection"""
    conn = sqlite3.connect('finance.db')
    conn.row_factory = sqlite3.Row
    return conn

def init_budget_tables():
    """Initialize budget-related database tables"""
    conn = get_db_connection()
    c = conn.cursor()
    
    # Create budgets table if not exists
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
    
    # Create index for faster queries
    c.execute('''
        CREATE INDEX IF NOT EXISTS idx_budget_user_month 
        ON budgets (user_id, month)
    ''')
    
    conn.commit()
    conn.close()

# TASK 8: Monthly Budget Setting
@budget_bp.route('/')
@login_required
def budget_dashboard():
    """Display budget dashboard with current month's budgets"""
    conn = get_db_connection()
    c = conn.cursor()
    
    current_month = datetime.now().strftime('%Y-%m')
    
    # Get user's budgets for current month
    budgets = c.execute('''
        SELECT id, category, amount, month
        FROM budgets 
        WHERE user_id = ? AND month = ?
        ORDER BY category
    ''', (current_user.id, current_month)).fetchall()
    
    # Get total budget amount
    total_budget = c.execute('''
        SELECT COALESCE(SUM(amount), 0) as total
        FROM budgets 
        WHERE user_id = ? AND month = ?
    ''', (current_user.id, current_month)).fetchone()['total']
    
    conn.close()
    
    return render_template('budget/dashboard.html', 
                         budgets=budgets, 
                         current_month=current_month,
                         total_budget=total_budget,
                         month_name=calendar.month_name[datetime.now().month])

@budget_bp.route('/set', methods=['GET', 'POST'])
@login_required
def set_budget():
    """Set or update monthly budget for a category"""
    if request.method == 'POST':
        category = request.form.get('category')
        amount = float(request.form.get('amount', 0))
        month = request.form.get('month', datetime.now().strftime('%Y-%m'))
        
        if amount <= 0:
            flash('Budget amount must be greater than 0', 'error')
            return redirect(url_for('budget.set_budget'))
        
        conn = get_db_connection()
        c = conn.cursor()
        
        try:
            # Check if budget exists for this category and month
            existing = c.execute('''
                SELECT id FROM budgets 
                WHERE user_id = ? AND category = ? AND month = ?
            ''', (current_user.id, category, month)).fetchone()
            
            if existing:
                # Update existing budget
                c.execute('''
                    UPDATE budgets 
                    SET amount = ?, updated_at = CURRENT_TIMESTAMP
                    WHERE id = ?
                ''', (amount, existing['id']))
                flash(f'Budget for {category} updated successfully!', 'success')
            else:
                # Insert new budget
                c.execute('''
                    INSERT INTO budgets (user_id, category, amount, month)
                    VALUES (?, ?, ?, ?)
                ''', (current_user.id, category, amount, month))
                flash(f'Budget for {category} set successfully!', 'success')
            
            conn.commit()
        except Exception as e:
            conn.rollback()
            flash(f'Error setting budget: {str(e)}', 'error')
        finally:
            conn.close()
        
        return redirect(url_for('budget.budget_dashboard'))
    
    # GET request - show form
    categories = ['Food', 'Transportation', 'Entertainment', 'Shopping', 
                 'Utilities', 'Healthcare', 'Education', 'Other']
    
    return render_template('budget/set_budget.html', categories=categories)

@budget_bp.route('/edit/<int:budget_id>', methods=['GET', 'POST'])
@login_required
def edit_budget(budget_id):
    """Edit existing budget"""
    conn = get_db_connection()
    c = conn.cursor()
    
    # Get budget details
    budget = c.execute('''
        SELECT * FROM budgets 
        WHERE id = ? AND user_id = ?
    ''', (budget_id, current_user.id)).fetchone()
    
    if not budget:
        flash('Budget not found', 'error')
        return redirect(url_for('budget.budget_dashboard'))
    
    if request.method == 'POST':
        amount = float(request.form.get('amount', 0))
        
        if amount <= 0:
            flash('Budget amount must be greater than 0', 'error')
        else:
            c.execute('''
                UPDATE budgets 
                SET amount = ?, updated_at = CURRENT_TIMESTAMP
                WHERE id = ?
            ''', (amount, budget_id))
            conn.commit()
            flash('Budget updated successfully!', 'success')
            return redirect(url_for('budget.budget_dashboard'))
    
    conn.close()
    return render_template('budget/edit_budget.html', budget=budget)

@budget_bp.route('/delete/<int:budget_id>')
@login_required
def delete_budget(budget_id):
    """Delete a budget"""
    conn = get_db_connection()
    c = conn.cursor()
    
    c.execute('''
        DELETE FROM budgets 
        WHERE id = ? AND user_id = ?
    ''', (budget_id, current_user.id))
    
    conn.commit()
    conn.close()
    
    flash('Budget deleted successfully!', 'success')
    return redirect(url_for('budget.budget_dashboard'))

# TASK 9: Budget Progress Visualization
@budget_bp.route('/progress')
@login_required
def budget_progress():
    """Display budget progress with visual bars"""
    conn = get_db_connection()
    c = conn.cursor()
    
    current_month = datetime.now().strftime('%Y-%m')
    
    # Get budgets for current month
    budgets = c.execute('''
        SELECT category, amount
        FROM budgets 
        WHERE user_id = ? AND month = ?
        ORDER BY category
    ''', (current_user.id, current_month)).fetchall()
    
    progress_data = []
    total_budget = 0
    total_spent = 0
    
    for budget in budgets:
        category = budget['category']
        budget_amount = budget['amount']
        total_budget += budget_amount
        
        # Calculate spending for this category
        spent = c.execute('''
            SELECT COALESCE(SUM(amount), 0) as total
            FROM transactions 
            WHERE user_id = ? 
            AND category = ? 
            AND strftime('%Y-%m', date) = ?
            AND type = 'expense'
        ''', (current_user.id, category, current_month)).fetchone()['total']
        
        total_spent += spent
        
        # Calculate percentage and determine status
        percentage = (spent / budget_amount * 100) if budget_amount > 0 else 0
        remaining = budget_amount - spent
        
        # Determine color and status based on percentage
        if percentage <= 50:
            color = 'success'  # Green
            status = 'On Track'
        elif percentage <= 80:
            color = 'warning'  # Yellow
            status = 'Caution'
        elif percentage <= 100:
            color = 'danger-orange'  # Orange
            status = 'Warning'
        else:
            color = 'danger'  # Red
            status = 'Over Budget!'
        
        progress_data.append({
            'category': category,
            'budget_amount': budget_amount,
            'spent': spent,
            'remaining': remaining,
            'percentage': min(percentage, 100),  # Cap at 100% for display
            'actual_percentage': percentage,  # Actual percentage for data
            'color': color,
            'status': status,
            'is_over': spent > budget_amount
        })
    
    # Sort by percentage (highest first)
    progress_data.sort(key=lambda x: x['actual_percentage'], reverse=True)
    
    # Calculate overall statistics
    overall_percentage = (total_spent / total_budget * 100) if total_budget > 0 else 0
    
    stats = {
        'total_budget': total_budget,
        'total_spent': total_spent,
        'total_remaining': total_budget - total_spent,
        'overall_percentage': overall_percentage,
        'categories_over_budget': sum(1 for p in progress_data if p['is_over']),
        'categories_on_track': sum(1 for p in progress_data if p['percentage'] <= 50)
    }
    
    conn.close()
    
    return render_template('budget/progress.html', 
                         progress_data=progress_data,
                         stats=stats,
                         current_month=current_month,
                         month_name=calendar.month_name[datetime.now().month])

@budget_bp.route('/api/progress/<category>')
@login_required
def api_budget_progress(category):
    """API endpoint for getting budget progress for a specific category"""
    conn = get_db_connection()
    c = conn.cursor()
    
    current_month = datetime.now().strftime('%Y-%m')
    
    # Get budget for category
    budget = c.execute('''
        SELECT amount FROM budgets 
        WHERE user_id = ? AND category = ? AND month = ?
    ''', (current_user.id, category, current_month)).fetchone()
    
    if not budget:
        return jsonify({'error': 'Budget not found'}), 404
    
    budget_amount = budget['amount']
    
    # Get spending
    spent = c.execute('''
        SELECT COALESCE(SUM(amount), 0) as total
        FROM transactions 
        WHERE user_id = ? AND category = ? 
        AND strftime('%Y-%m', date) = ? AND type = 'expense'
    ''', (current_user.id, category, current_month)).fetchone()['total']
    
    conn.close()
    
    percentage = (spent / budget_amount * 100) if budget_amount > 0 else 0
    
    return jsonify({
        'category': category,
        'budget': budget_amount,
        'spent': spent,
        'remaining': budget_amount - spent,
        'percentage': percentage,
        'status': 'over' if spent > budget_amount else 'ok'
    })

@budget_bp.route('/alerts')
@login_required
def budget_alerts():
    """Get budget alerts for categories approaching or exceeding limits"""
    conn = get_db_connection()
    c = conn.cursor()
    
    current_month = datetime.now().strftime('%Y-%m')
    
    # Get all budgets with spending > 80%
    alerts = c.execute('''
        SELECT 
            b.category,
            b.amount as budget_amount,
            COALESCE(SUM(t.amount), 0) as spent,
            (COALESCE(SUM(t.amount), 0) / b.amount * 100) as percentage
        FROM budgets b
        LEFT JOIN transactions t ON 
            t.user_id = b.user_id AND 
            t.category = b.category AND 
            strftime('%Y-%m', t.date) = b.month AND
            t.type = 'expense'
        WHERE b.user_id = ? AND b.month = ?
        GROUP BY b.category, b.amount
        HAVING percentage > 80
        ORDER BY percentage DESC
    ''', (current_user.id, current_month)).fetchall()
    
    conn.close()
    
    alert_list = []
    for alert in alerts:
        if alert['percentage'] > 100:
            level = 'danger'
            message = f"Over budget by ${alert['spent'] - alert['budget_amount']:.2f}"
        elif alert['percentage'] > 90:
            level = 'warning'
            message = f"Only ${alert['budget_amount'] - alert['spent']:.2f} remaining"
        else:
            level = 'info'
            message = f"{alert['percentage']:.0f}% of budget used"
        
        alert_list.append({
            'category': alert['category'],
            'level': level,
            'message': message,
            'percentage': alert['percentage']
        })
    
    return jsonify(alert_list)

# Helper function for other modules
def get_budget_summary(user_id, month=None):
    """Get budget summary for a user"""
    if month is None:
        month = datetime.now().strftime('%Y-%m')
    
    conn = get_db_connection()
    c = conn.cursor()
    
    summary = c.execute('''
        SELECT 
            COUNT(*) as total_categories,
            SUM(amount) as total_budget,
            MIN(amount) as min_budget,
            MAX(amount) as max_budget,
            AVG(amount) as avg_budget
        FROM budgets 
        WHERE user_id = ? AND month = ?
    ''', (user_id, month)).fetchone()
    
    conn.close()
    
    return dict(summary) if summary else None
