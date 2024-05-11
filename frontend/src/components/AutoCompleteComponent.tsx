import React, { useState } from "react";
// @ts-ignore
import Autosuggest from "react-autosuggest";

const theme = {
  input: {
    height: '35px',
    fontSize: '1.2rem',
    padding: '10px',
    width: '100%',
    boxSizing: 'border-box',
    border: '1px solid',
    borderRadius: '4px',
  },
  suggestionsList: {
    margin: 0,
    padding: 0,
    listStyleType: 'none',
    backgroundColor: '#333333',
    border: '1px solid',
    borderRadius: '4px',
  },
  suggestion: {
    padding: '10px',
    cursor: 'pointer',
  },
  suggestionHighlighted: {
    padding: '10px',
    cursor: 'pointer',
    backgroundColor: '#666666', // Farbe für hervorgehobene Vorschläge
  },
};

const AutoCompleteComponent = ({ onSongSelect }: {onSongSelect: any}) => {
  const [value, setValue] = useState("");
  const [suggestions, setSuggestions] = useState([]);

  const getSuggestions = async (inputValue: string) => {
    try {
      const response = await fetch(
        `http://localhost:5000/api/search?q=${inputValue}`
      );
      const data = await response.json();
      return data.suggestions;
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
  const onSuggestionSelected = (event, { suggestion }) => {
    console.log("Selected suggestion:", suggestion);
    onSongSelect(suggestion.title); // Pass the selected title back to the parent component
  };

  const inputProps = {
    placeholder: "Search for a song",
    value,
    // @ts-ignore
    onChange: (_, { newValue }) => setValue(newValue),
  };

  return (
    <Autosuggest
      theme={theme}
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
