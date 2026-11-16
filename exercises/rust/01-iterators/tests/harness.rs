mod scores;
use scores::*;

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn average_of_passing_scores() {
        let scores = vec![40, 75, 90, 49, 50];
        assert_eq!(passing_average(&scores, 50), Some(215.0 / 3.0));
    }

    #[test]
    fn average_none_when_nobody_passes() {
        assert_eq!(passing_average(&vec![1, 2, 3], 50), None);
        assert_eq!(passing_average(&vec![], 0), None);
    }

    #[test]
    fn initials_skip_empty_names() {
        let names: Vec<String> = ["ada", "", "grace", "Linus"].iter().map(|s| s.to_string()).collect();
        assert_eq!(initials(&names), "AGL");
    }

    #[test]
    fn initials_handle_non_ascii() {
        let names = vec!["élodie".to_string(), "zoë".to_string()];
        assert_eq!(initials(&names), "éZ");
    }

    #[test]
    fn longest_word_first_wins_ties() {
        let text = String::from("the quick brown fox jumped");
        assert_eq!(longest_word(&text).as_deref(), Some("jumped"));
        let tie = String::from("one two six");
        assert_eq!(longest_word(&tie).as_deref(), Some("one"));
    }

    #[test]
    fn longest_word_of_blank_text() {
        assert_eq!(longest_word(&String::from("   ")), None);
    }
}
