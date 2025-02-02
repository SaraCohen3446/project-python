CREATE DATABASE RecipeManagement;
GO

-- ����� ����� �������
USE RecipeManagement;
GO

-- ����� ���� Users
CREATE TABLE Users (
    UserID INT PRIMARY KEY IDENTITY(1,1),   -- ���� ����� ������, �������
    Username NVARCHAR(100) NOT NULL,         -- �� �����
    Email NVARCHAR(200) NOT NULL,            -- ����� ���"�
    Password NVARCHAR(255) NOT NULL,         -- �����
    DateCreated DATETIME DEFAULT GETDATE()   -- ����� ����� ������
);
GO

-- ����� ���� Recipes
CREATE TABLE Recipes (
    RecipeID INT PRIMARY KEY IDENTITY(1,1),   -- ���� ����� ������, �������
    UserID INT,                                -- ���� ������ ���� �� ������
    Title NVARCHAR(255) NOT NULL,              -- �� ������
    Description NVARCHAR(MAX),                 -- ����� ������
    Ingredients NVARCHAR(MAX),                 -- ����� �������
    Instructions NVARCHAR(MAX),                -- ������ ����
    DateCreated DATETIME DEFAULT GETDATE(),    -- ����� ����� ������
    CONSTRAINT FK_Recipes_Users FOREIGN KEY (UserID) REFERENCES Users(UserID) -- ��� �� ���� Users
);
GO

-- ����� ���� Comments
CREATE TABLE Comments (
    CommentID INT PRIMARY KEY IDENTITY(1,1),  -- ���� ���� ������, �������
    RecipeID INT,                              -- ���� ������
    UserID INT,                                -- ���� ������ ������ �� �����
    Content NVARCHAR(MAX) NOT NULL,            -- ���� �����
    DateCreated DATETIME DEFAULT GETDATE(),    -- ����� ����� �����
    CONSTRAINT FK_Comments_Recipes FOREIGN KEY (RecipeID) REFERENCES Recipes(RecipeID), -- ��� �� ���� Recipes
    CONSTRAINT FK_Comments_Users FOREIGN KEY (UserID) REFERENCES Users(UserID)  -- ��� �� ���� Users
);
GO
