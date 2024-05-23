import { createTheme, useMediaQuery } from "@mui/material";
import Cookies from "js-cookie";
import React, { useMemo, useState } from "react";
// @ts-ignore
import Autosuggest from "react-autosuggest";

const AutoCompleteComponent = ({
  onSongSelect,
  onSongDownload,
}: {
  onSongSelect: (new_song: string) => void;
  onSongDownload: (url: string) => void;
}) => {
  const [value, setValue] = useState("");
  const [suggestions, setSuggestions] = useState([]);
  const prefersDarkMode = useMediaQuery("(prefers-color-scheme: dark)");
  const theme = useMemo(
    () =>
      createTheme({
        palette: {
          mode: prefersDarkMode ? "dark" : "light",
        },
      }),
    [prefersDarkMode]
  );

  const themeStyling = {
    input: {
      height: "35px",
      fontSize: "1.2rem",
      padding: "10px",
      minWidth: "390px",
      boxSizing: "border-box",
      border: "1px solid",
      borderRadius: "4px",
    },
    suggestionsList: {
      margin: 0,
      padding: 0,
      listStyleType: "none",
      backgroundColor:
        theme.palette.mode === "dark" ? "#333333" : "rgba(102, 102, 102,0.2)", // Farbe für hervorgehobene Vorschläge
      border: "1px solid",
      borderRadius: "4px",
      maxWidth: "390px",
    },
    suggestion: {
      padding: "10px",
      cursor: "pointer",
    },
    suggestionHighlighted: {
      padding: "10px",
      cursor: "pointer",
      backgroundColor:
        theme.palette.mode === "dark" ? "#666666" : "rgba(102, 102, 102,0.5)", // Farbe für hervorgehobene Vorschläge
    },
  };

  const textColor =
    theme.palette.mode === "dark" ? "white" : "rgba(0, 0, 0, 0.87)";

  const getSuggestions = async (inputValue: string) => {
    try {
      const response = await fetch(
        `http://localhost:5000/api/search?q=${inputValue}`
      );
      const data = await response.json();
      // Limit the suggestions to a maximum of 10
      return data.suggestions.slice(0, 10);
    } catch (error) {
      console.error("Error fetching suggestions:", error);
      return [];
    }
  };
  // @ts-ignore
  const onSuggestionsFetchRequested = async ({ value }) => {
    const suggestions = await getSuggestions(value);
    setSuggestions(suggestions);
  };

  const onSuggestionsClearRequested = () => {
    setSuggestions([]);
  };

  // @ts-ignore
  const onSuggestionSelected = async (event, { suggestion }) => {
    try {
      onSongSelect(suggestion.title);
    } catch (error) {
      console.error("Error sending selected song to backend:", error);
    }
    setValue("");
  };

  const handleKeyDown = async (
    event: React.KeyboardEvent<HTMLInputElement>
  ) => {
    if (event.key === "Enter") {
      try {
        onSongDownload(value);
      } catch (error) {
        console.error("Error downloading the song:", error);
      }
    }
  };

  const inputProps = {
    placeholder: "Search for a song or paste a YouTube link",
    value,
    // @ts-ignore
    onChange: (_, { newValue }) => setValue(newValue),
    onKeyDown: handleKeyDown,
  };

  return (
    <Autosuggest
      theme={themeStyling}
      suggestions={suggestions}
      onSuggestionsFetchRequested={onSuggestionsFetchRequested}
      onSuggestionsClearRequested={onSuggestionsClearRequested}
      onSuggestionSelected={onSuggestionSelected}
      // @ts-ignore
      getSuggestionValue={(suggestion) => suggestion.title}
      // @ts-ignore
      renderSuggestion={(suggestion) => <div>{suggestion.title}</div>}
      inputProps={inputProps}
    />
  );
};

export default AutoCompleteComponent;
