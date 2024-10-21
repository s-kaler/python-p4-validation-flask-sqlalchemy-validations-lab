from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import validates
db = SQLAlchemy()

class Author(db.Model):
    __tablename__ = 'authors'
    
    id = db.Column(db.Integer, primary_key=True)
    name= db.Column(db.String, unique=True, nullable=False)
    phone_number = db.Column(db.String)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, onupdate=db.func.now())

    # Add validators 
    @validates('name')
    def validate_name(self, key, value):
        if not value:
            raise ValueError('Name is required')
        else:
            existing_names = [author.name for author in Author.query.all()]
            if value in existing_names:
                raise ValueError('Name must be unique')
        return value
    
    @validates('phone_number')
    def validate_phone_number(self, key, value):
        if not value:
            raise ValueError('Phone number is required')
        elif len(value) != 10:
            raise ValueError('Phone number must be exactly 10 digits')
        elif not value.isdigit():
            raise ValueError('Phone number must only contain digits')
        return value
    

    def __repr__(self):
        return f'Author(id={self.id}, name={self.name})'

class Post(db.Model):
    __tablename__ = 'posts'
    
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String, nullable=False)
    content = db.Column(db.String)
    category = db.Column(db.String)
    summary = db.Column(db.String)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, onupdate=db.func.now())

    # Add validators  
    @validates('title')
    def validate_title(self, key, value):
        valid_keywords = ["Won't Believe", "Secret", "Top", "Guess"]
        is_keyword = False
        for keyword in valid_keywords:
            if keyword in value:
                is_keyword = True
        if not value:
            raise ValueError('Title is required')
        elif not is_keyword:
            raise ValueError('Title must be one of: Won\'t Believe, Secret, Top, Guess')
        return value
    
    @validates('content')
    def validate_content(self, key, value):
        if not value:
            raise ValueError('Content is required')
        elif len(value) < 250:
            raise ValueError('Content must be at least 250 characters long')
        return value

    @validates('summary')
    def validate_summary(self, key, value):
        if not value:
            raise ValueError('Summary is required')
        elif len(value) > 250:
            raise ValueError('Summary must be at most 250 characters long')
        return value
    
    @validates('category')
    def validate_category(self, key, value):
        if not value:
            raise ValueError('Category is required')
        elif not value in ["Fiction", "Non-Fiction"]:
            raise ValueError('Category must be one of: Fiction, Non-Fiction')
        return value

    def __repr__(self):
        return f'Post(id={self.id}, title={self.title} content={self.content}, summary={self.summary})'
