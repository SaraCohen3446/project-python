CREATE DATABASE RecipeManagement;
GO

-- שימוש במאגר הנתונים
USE RecipeManagement;
GO

-- יצירת טבלת Users
CREATE TABLE Users (
    UserID INT PRIMARY KEY IDENTITY(1,1),   -- מזהה משתמש ייחודי, אוטומטי
    Username NVARCHAR(100) NOT NULL,         -- שם משתמש
    Email NVARCHAR(200) NOT NULL,            -- כתובת דוא"ל
    Password NVARCHAR(255) NOT NULL,         -- סיסמה
    DateCreated DATETIME DEFAULT GETDATE()   -- תאריך יצירת המשתמש
);
GO

-- יצירת טבלת Recipes
CREATE TABLE Recipes (
    RecipeID INT PRIMARY KEY IDENTITY(1,1),   -- מזהה מתכון ייחודי, אוטומטי
    UserID INT,                                -- מזהה המשתמש שיצר את המתכון
    Title NVARCHAR(255) NOT NULL,              -- שם המתכון
    Description NVARCHAR(MAX),                 -- תיאור המתכון
    Ingredients NVARCHAR(MAX),                 -- רשימת מרכיבים
    Instructions NVARCHAR(MAX),                -- הוראות הכנה
    DateCreated DATETIME DEFAULT GETDATE(),    -- תאריך יצירת המתכון
    CONSTRAINT FK_Recipes_Users FOREIGN KEY (UserID) REFERENCES Users(UserID) -- קשר עם טבלת Users
);
GO

-- יצירת טבלת Comments
CREATE TABLE Comments (
    CommentID INT PRIMARY KEY IDENTITY(1,1),  -- מזהה הערה ייחודי, אוטומטי
    RecipeID INT,                              -- מזהה המתכון
    UserID INT,                                -- מזהה המשתמש שהשאיר את ההערה
    Content NVARCHAR(MAX) NOT NULL,            -- תוכן ההערה
    DateCreated DATETIME DEFAULT GETDATE(),    -- תאריך יצירת ההערה
    CONSTRAINT FK_Comments_Recipes FOREIGN KEY (RecipeID) REFERENCES Recipes(RecipeID), -- קשר עם טבלת Recipes
    CONSTRAINT FK_Comments_Users FOREIGN KEY (UserID) REFERENCES Users(UserID)  -- קשר עם טבלת Users
);
GO
