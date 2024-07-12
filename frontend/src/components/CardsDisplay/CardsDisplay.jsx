// Component to show a list of cards on the frontend


export const CardsDisplay = ({ cards }) => {
    return (
        <div style={{display: "flex", flexWrap: "wrap", justifyContent: "center", gap: "10px", backgroundColor:"dimgray", padding: "10px"}}>
            {cards}
        </div>
    );
}
