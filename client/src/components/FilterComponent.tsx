import React from 'react';

const FilterComponent = () => {
    return (
        <div style={{ width: 400, paddingLeft: 48, paddingRight: 48, background: 'white', boxShadow: '0px 0px 5px 2px rgba(0, 0, 0, 0.25)', overflow: 'hidden', flexDirection: 'column', justifyContent: 'flex-start', alignItems: 'center', gap: 30, display: 'inline-flex' }}>
            <div style={{ width: 282, justifyContent: 'center', alignItems: 'flex-start', gap: 95, display: 'inline-flex' }}>
                <span style={{ fontSize: 32, fontFamily: 'Inter', fontWeight: '400', color: 'black' }}>Filters</span>
            </div>
            <div style={{ alignSelf: 'stretch', flexDirection: 'column', justifyContent: 'flex-start', alignItems: 'center', gap: 10, display: 'flex' }}>
                {[...Array(5)].map((_, index) => (
                    <div key={index} style={{ alignSelf: 'stretch', height: 40, justifyContent: 'flex-start', alignItems: 'center', gap: 10, display: 'inline-flex' }}>
                        <input type="checkbox" style={{ width: 40, height: 40 }} />
                        <span style={{ fontSize: 14, fontFamily: 'Inter', fontWeight: '400', color: 'black' }}>Filter</span>
                        <input type="text" placeholder="Enter value" style={{ width: 150, height: 30, borderRadius: 4, outline: '1px solid #9BA1A6', padding: '6px 27px', background: '#D9D9D9' }} />
                    </div>
                ))}
            </div>
            <div style={{ paddingTop: 15, paddingBottom: 15, justifyContent: 'center', alignItems: 'center', gap: 15, display: 'inline-flex' }}>
                <button style={{ width: 100, height: 40, background: '#007BFF', borderRadius: 6, color: 'white', fontSize: 16, fontWeight: 'bold', border: 'none', cursor: 'pointer' }}>Submit</button>
                <button style={{ width: 100, height: 40, background: '#D9D9D9', borderRadius: 6, color: 'black', fontSize: 16, fontWeight: 'bold', border: 'none', cursor: 'pointer' }}>Cancel</button>
            </div>
        </div>
);
};

export default FilterComponent;
