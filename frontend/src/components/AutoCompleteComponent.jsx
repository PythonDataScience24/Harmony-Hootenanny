import React, { useState } from "react";
import Autosuggest from "react-autosuggest";

const AutoCompleteComponent = ({ onSongSelect }) => {
  const [value, setValue] = useState("");
  const [suggestions, setSuggestions] = useState([]);

  const getSuggestions = async (inputValue) => {
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

  const onSuggestionsFetchRequested = async ({ value }) => {
    const suggestions = await getSuggestions(value);
    setSuggestions(suggestions);
  };

  const onSuggestionsClearRequested = () => {
    setSuggestions([]);
  };

  const onSuggestionSelected = (event, { suggestion }) => {
    console.log("Selected suggestion:", suggestion);
    onSongSelect(suggestion.title); // Pass the selected title back to the parent component
  };

  const inputProps = {
    placeholder: "Search for a song",
    value,
    onChange: (_, { newValue }) => setValue(newValue),
  };

  return (
    <Autosuggest
      suggestions={suggestions}
      onSuggestionsFetchRequested={onSuggestionsFetchRequested}
      onSuggestionsClearRequested={onSuggestionsClearRequested}
      onSuggestionSelected={onSuggestionSelected}
      getSuggestionValue={(suggestion) => suggestion.title}
      renderSuggestion={(suggestion) => <div>{suggestion.title}</div>}
      inputProps={inputProps}
    />
  );
};

export default AutoCompleteComponent;
