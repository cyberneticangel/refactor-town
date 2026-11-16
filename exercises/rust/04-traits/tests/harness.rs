mod catalog;
use catalog::*;

#[cfg(test)]
mod tests {
    use super::*;

    fn book() -> Book {
        Book { title: "Dune".into(), author: "Frank Herbert".into(), year: 1965 }
    }
    fn movie() -> Movie {
        Movie { title: "Arrival".into(), director: "Denis Villeneuve".into(), year: 2016 }
    }
    fn album() -> Album {
        Album { title: "Kind of Blue".into(), artist: "Miles Davis".into(), year: 1959 }
    }

    #[test]
    fn summaries() {
        assert_eq!(book().summary(), "[Book] Dune (1965) by Frank Herbert");
        assert_eq!(movie().summary(), "[Movie] Arrival (2016) by Denis Villeneuve");
        assert_eq!(album().summary(), "[Album] Kind of Blue (1959) by Miles Davis");
    }

    #[test]
    fn classics_are_fifty_years_or_older() {
        assert!(book().is_classic());
        assert!(!movie().is_classic());
        let edge = Movie { title: "Jaws".into(), director: "Steven Spielberg".into(), year: 1976 };
        assert!(edge.is_classic());
        let not_yet = Album { title: "Rumours".into(), artist: "Fleetwood Mac".into(), year: 1977 };
        assert!(!not_yet.is_classic());
    }

    #[test]
    fn full_report() {
        let report = catalog_report(&[book()], &[movie()], &[album()]);
        assert_eq!(
            report,
            "[Book] Dune (1965) by Frank Herbert *\n\
             [Movie] Arrival (2016) by Denis Villeneuve\n\
             [Album] Kind of Blue (1959) by Miles Davis *\n\
             3 items, 2 classics"
        );
    }

    #[test]
    fn empty_report() {
        assert_eq!(catalog_report(&[], &[], &[]), "0 items, 0 classics");
    }
}
