const CURRENT_YEAR: u32 = 2026;
const CLASSIC_AGE: u32 = 50;

/// Anything that can appear in the catalog. Implementors provide the facts;
/// the trait provides the shared behaviour.
pub trait CatalogItem {
    fn kind(&self) -> &str;
    fn title(&self) -> &str;
    fn creator(&self) -> &str;
    fn year(&self) -> u32;

    fn summary(&self) -> String {
        format!("[{}] {} ({}) by {}", self.kind(), self.title(), self.year(), self.creator())
    }

    fn is_classic(&self) -> bool {
        CURRENT_YEAR - self.year() >= CLASSIC_AGE
    }
}

pub struct Book {
    pub title: String,
    pub author: String,
    pub year: u32,
}

pub struct Movie {
    pub title: String,
    pub director: String,
    pub year: u32,
}

pub struct Album {
    pub title: String,
    pub artist: String,
    pub year: u32,
}

impl CatalogItem for Book {
    fn kind(&self) -> &str { "Book" }
    fn title(&self) -> &str { &self.title }
    fn creator(&self) -> &str { &self.author }
    fn year(&self) -> u32 { self.year }
}

impl CatalogItem for Movie {
    fn kind(&self) -> &str { "Movie" }
    fn title(&self) -> &str { &self.title }
    fn creator(&self) -> &str { &self.director }
    fn year(&self) -> u32 { self.year }
}

impl CatalogItem for Album {
    fn kind(&self) -> &str { "Album" }
    fn title(&self) -> &str { &self.title }
    fn creator(&self) -> &str { &self.artist }
    fn year(&self) -> u32 { self.year }
}

fn report_line(item: &dyn CatalogItem) -> String {
    let marker = if item.is_classic() { " *" } else { "" };
    format!("{}{}", item.summary(), marker)
}

pub fn catalog_report(books: &[Book], movies: &[Movie], albums: &[Album]) -> String {
    let items: Vec<&dyn CatalogItem> = books
        .iter()
        .map(|b| b as &dyn CatalogItem)
        .chain(movies.iter().map(|m| m as &dyn CatalogItem))
        .chain(albums.iter().map(|a| a as &dyn CatalogItem))
        .collect();

    let classics = items.iter().filter(|item| item.is_classic()).count();
    let mut lines: Vec<String> = items.iter().map(|item| report_line(*item)).collect();
    lines.push(format!("{} items, {} classics", items.len(), classics));
    lines.join("\n")
}
