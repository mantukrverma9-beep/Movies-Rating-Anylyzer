import pandas as pd
import matplotlib.pyplot as plt

def load_data():
    try:
        df = pd.read_csv("movies.csv", dtype=str)
        df.columns = df.columns.str.strip()
        
        requrired_columns = ["Movie", "Genre", "Rating"]
        
        if not all(col in df.columns for col in requrired_columns):
            print("Error: CSV must contain Movies, Genre and Rating columns.")
            
            return None
        
        valid_row = []
        for index, row in df.iterrows():
            movie = row["Movie"]
            genre = row["Genre"]
            rating = row["Rating"]
            
            if pd.isna(movie) or not movie.strip():
                print(f"Row {index + 1}: Missing movie name. Skipped.")
                continue
            
            if pd.isna(genre) or not genre.strip():
                print(f"Row {index + 1}: Missing genre. Skipped.")
                continue
            
            try:
                rating = float(rating)
                
            except (ValueError, TypeError):
                print(f"Row {index + 1} skipped: invalid Rating '{rating}'.")
                continue
            
            if rating < 0 or rating > 10:
                print(f"Row {index + 1} skipped: Rating {rating:g} must be between 0 and 10")
                continue
            
            valid_row.append({
                "Movie" : movie.strip(),
                "Genre" : genre.strip(),
                "Rating" : rating
            })
            
        clean_df = pd.DataFrame(valid_row)
        print("\nValid Rows", len(clean_df))
        return clean_df
    
    except FileNotFoundError:
        print("Error: movies.csv file  not found.")
        
        return None
    
    except Exception as e:
        print("Error", e)
        return None
    
    # movies summary
def movie_summary(df):
    average = df["Rating"].mean()
        
    top_movie =df.loc[df["Rating"].idxmax()]
        
    lowest_movie = df.loc[df["Rating"].idxmin()]
        
    print("\n==== MOVIE SUMMARY ====")
    print(f"Average rating: {average:.2f}")
        
    print(
        f"Top rated:  {top_movie['Movie']}" 
        f"({top_movie['Rating']:g})"
        )
        
    print(
        f"Lowest: {lowest_movie['Movie']}" 
        f"({lowest_movie['Rating']:g})"
        )
        
        
def genre_analysis(df):
    
    genre_avg = df.groupby("Genre")["Rating"].mean()
    
    print("\n===== GENRE-WISE AVERAGE =====")
    
    for genre, rating in genre_avg.items():
        print(f"{genre}: {rating:.2f}")
        
    best_genre = genre_avg.idxmax()
    print(f"\nBest genre:", best_genre)
    
    plt.figure(figsize=(8, 5))
    bars = plt.bar(
        genre_avg.index,
        genre_avg.values,
        edgecolor="black"
        
    )
    genre_avg.plot(kind="bar")
    
    plt.title("Genre-wise Average Rating")
    plt.xlabel("Genre")
    plt.ylabel("Average Rating")
    plt.ylim(0, 10)
    
    for bar in bars:
        height = bar.get_height()
        
        plt.text(
            bar.get_x() + bar.get_width() / 2,
            height + 0.1,
            f"{height:.2f}",
            ha="center"
        )
        
    plt.grid(axis="y", linestyle="--", alpha=0.5)
    plt.tight_layout()
    
    plt.show()
    
def show_histogram(df):
    plt.figure(figsize=(8, 5))
    
    plt.hist(df["Rating"], bins=10, edgecolor = "black")
    plt.title("Movie Rating Distribution")
    plt.xlabel("Movie Rating")
    plt.ylabel("Number of movies")
    plt.tight_layout()
    plt.show()
    
    
def main():
    df = load_data()
    
    if df is None or df.empty:
        print("No valid movie data available.")
        return
    
    while True:
        print("\n==== MOVIE RATING ANALYZER ====")
        print("1. Summary")
        print("2. Genre-wise Average")
        print("3. Exit")
        
        choice = input("\nEnter your choice: ")
        
        if choice == "1":
            movie_summary(df)
            
        elif choice == "2":
            genre_analysis(df)
            show_histogram(df)
            
        elif choice == "3":
            print("Thank you for using Movie Rating Analyzer!")
            break
        else:
            print("Invalid choice! Please select 1, 2 and 3.")
            
            
if __name__ == "__main__":
    main()