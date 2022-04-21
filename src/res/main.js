function displayActivePlaylist(playlist, linkToPlaylist) {
    playlist.classList.add("active");
    playlist.scrollTop = playlist.scrollHeight;
    linkToPlaylist.classList.add("active-playlist");
}

window.onload = function(event) {
    let firstPlaylist = document.querySelectorAll(".single-playlist")[0];
    let firstPlaylistPartnerLink = document.querySelectorAll("a")[0];
    displayActivePlaylist(firstPlaylist, firstPlaylistPartnerLink);

    links = document.querySelectorAll(".playlists-list a").forEach(function(link){
        link.addEventListener("click", function(event) {
            event.preventDefault();
            document.querySelector(".active").classList.remove("active");
            document.querySelector(".active-playlist").classList.remove("active-playlist");

            let target = link.hash.replace("#","");
            playlist = document.querySelector(`[data-playlistid="${target}"]`);
            displayActivePlaylist(playlist, link);
        }, false);
    });
}
