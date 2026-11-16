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

impl Book {
    pub fn summary(&self) -> String {
        format!("[Book] {} ({}) by {}", self.title, self.year, self.author)
    }

    pub fn is_classic(&self) -> bool {
        2026 - self.year >= 50
    }
}

impl Movie {
    pub fn summary(&self) -> String {
        format!("[Movie] {} ({}) by {}", self.title, self.year, self.director)
    }

    pub fn is_classic(&self) -> bool {
        2026 - self.year >= 50
    }
}

impl Album {
    pub fn summary(&self) -> String {
        format!("[Album] {} ({}) by {}", self.title, self.year, self.artist)
    }

    pub fn is_classic(&self) -> bool {
        2026 - self.year >= 50
    }
}

pub fn catalog_report(books: &[Book], movies: &[Movie], albums: &[Album]) -> String {
    let mut lines = Vec::new();
    let mut classics = 0;
    for b in books {
        let mut line = b.summary();
        if b.is_classic() {
            line.push_str(" *");
            classics += 1;
        }
        lines.push(line);
    }
    for m in movies {
        let mut line = m.summary();
        if m.is_classic() {
            line.push_str(" *");
            classics += 1;
        }
        lines.push(line);
    }
    for a in albums {
        let mut line = a.summary();
        if a.is_classic() {
            line.push_str(" *");
            classics += 1;
        }
        lines.push(line);
    }
    lines.push(format!("{} items, {} classics", lines.len(), classics));
    lines.join("\n")
}
